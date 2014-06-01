#-*-coding:utf-8-*-
"""
@package btractor.tests.submission
@brief tests for btractor.submission

@note we use this module to test all of the submission implementations roughly
@author Sebastian Thiel
@copyright [GNU Lesser General Public License](https://www.gnu.org/licenses/lgpl.html)
"""
from __future__ import unicode_literals
from butility.future import str

__all__ = []

import os
import sys
import subprocess

from butility.tests import (TestCase,
                            with_rw_directory)


from btractor.alf import (Job,
                          AlfSerializer)

from btractor.delegates import NukeTractorDelegate

from btractor.alf.generators import *
from btractor.submission import *

# Just to test * imports
from btractor.submission.plugins.maya import *
from btractor.submission.plugins.nuke import *
from btractor.submission.plugins.bash import *

from bapp.tests import with_application


class TestSubmission(TestCase):
    """Tests for nuke submission types"""
    __slots__ = ()
    
    # -------------------------
    ## @name Utilities
    # @{

    def _assert_stderr(self, stderr):
        """Make sure stderr is clean of errors"""
        assert 'WARNING' not in stderr and 'ERROR' not in stderr
    
    def _start_tractor_process(self, cmd):
        """@return the created process, with stdin, stdout and stderr redirected to a pipe
        @param cmd alf cmd operator to start"""
        return subprocess.Popen( [cmd.executable] + [str(i) for i in cmd.args], stdin = subprocess.PIPE,
                                    stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    ## -- End Utilities -- @}
    
    def test_submitter(self):
        """simple submitter test"""
        submit_success = 'OK job script accepted, jid: 1307140009'
        m = TractorSubmitter.re_job_id.search(submit_success)
        assert m and int(m.group(0)) == 1307140009 
    
    @with_application(from_file=__file__)
    def test_nuke_submission(self):
        """just run the nuke submission code"""
        nkjob = NukeRenderTasksChain().prepend_head(JobGenerator())
        context = nkjob.default_context()
        
        assert not nkjob.head().is_valid_context(context), 'we should require a nuke file'
        
        data = context.value_by_schema(nkjob.head().field_schema())
        
        # fake the nuke file, its really about being in a certain hierarchy
        data.job.file = 'foobar.nk'
        data.frame.last = 10
        data.frame.chunk_size = 1
        context.set_value_by_schema(nkjob.head().field_schema(), data)
        
        job = nkjob.head().generator(context).next()
        cmd = job.subtasks[0].subtasks[0].cmds[0]
        assert NukeRenderTaskGenerator.limit_nuke_render in cmd.tags
        assert cmd.retryrc == [NukeTractorDelegate.read_error_return_code]
        assert len(job.subtasks) == 11, 'unexpected chunking'
        assert isinstance(job, Job)
        
        # DEBUG
        # AlfSerializer().init(sys.stdout).serialize(job)
        
        # DEBUG - warning - creates a job on the farm just for your manual exmination
        # TODO: with the tractor API, we COULD delete it afterwards
        # NOTE: actually it doesn't create a job, as a service key is missing
        # assert TractorSubmitter().submit(job, paused=True) != 0
    
    @with_application(from_file=__file__)
    def test_maya_batch_submission(self):
        """Check if maya batch submission can generally work using a command feed from stdin"""
        chain = MayaBatchTaskChain().prepend_head(JobGenerator())
        jgen = chain.head()
        
        context = jgen.default_context()
        schema = jgen.field_schema()
        value = context.value_by_schema(schema)
        hello = 'hello world'
        value.maya.cmd.python = 'print "%s"; print data' % hello
        context.set_value_by_schema(schema, value)
        
        job = jgen.generator(context).next()
        
        # execute the command ourselves
        cmd = job.subtasks[0].cmds[0]
        process = self._start_tractor_process(cmd)
        
        process.stdin.write(cmd.msg)
        process.stdin.close()
        process.stdin = None
        stdout, stderr = process.communicate()
        
        self._assert_stderr(stderr), "the tractor-wrapper redirects everything to stdout"
        assert "TR_EXIT_STATUS" not in stdout
        assert hello in stdout, 'should have printed hello world' 
        assert process.returncode == 0, "should not have produced an error"
        # DEBUG
        # AlfSerializer().init(sys.stdout).serialize(job)
        
    @with_rw_directory
    def test_maya_render_submission(self, rw_dir):
        """Simple test including real rendering"""
        chain = FrameSequenceMayaRenderTaskChain().prepend_head(JobGenerator())
        jgen = chain.head()
        
        context = jgen.default_context()
        schema = jgen.field_schema()
        value = context.value_by_schema(schema)
        
        image_count = 0
        for test_render in ('mr', 'hw2'): 
            value.job.file = self.fixture_path('processing/tractor/submission/render-%s.ma' % test_render)
            assert value.job.file.isfile()
            value.frame.first = 2
            value.frame.last = 5
            value.maya.render.image_output_directory = rw_dir
            assert value.job.file.exists()
            
            context.set_value_by_schema(schema, value)
            job = jgen.generator(context).next()
            
            process = self._start_tractor_process(job.subtasks[0].subtasks[0].cmds[0])
            stdout, stderr = process.communicate()
            
            self._assert_stderr(stderr)
            assert process.returncode == 0
            
            new_image_count = len(list(rw_dir.walk(pattern='*.*')))
            assert new_image_count > image_count
            image_count = new_image_count
                    
            # DEBUG
            # AlfSerializer().init(sys.stdout).serialize(job)
        # end for each test-file
        
    def test_bash_executor(self):
        """Basic tests, just call code"""
        chain = BashTaskChain()
        
        context = chain.default_context()
        schema = chain.head().field_schema()
        data = context.value_by_schema(schema)
        data.batch.stdincmd = 'foo'
        data.batch.args = '{batch.stdincmd}'
        context.set_value_by_schema(schema, data)
        
        task = chain.generator(context).next()
        cmd = task.cmds[0]
        assert cmd.msg == 'foo', "substitution should have worked"
        assert cmd.args == ['foo']
        
# end class TestNukeSubmission
