#-*-coding:utf-8-*-
"""
@package btractor.tests.doc.test_examples

@copyright 2012 Sebastian Thiel
@author Sebastian Thiel
@copyright [GNU Lesser General Public License](https://www.gnu.org/licenses/lgpl.html)
"""
from __future__ import unicode_literals
__all__ = []

import sys

from butility.tests import (TestCase,
                            with_rw_directory)

from btractor.alf import (Job,
                          Cmd,
                          Instance,
                          Task,
                          Commands,
                          JobDate,
                          Assignments,
                          Assign,
                          AlfSerializer)


class TractorAlfTests(TestCase):
    """Tests alf structure setup and usage"""
    __slots__ = ()
    
    def test_base(self):
        """Static initializtation and dynamic adjustments"""
        ## [alf_task_init]
        task = Task('t1')
        assert task.title == 't1'
        
        # This is similar, but more explicit
        assert Task(title='t1').title == task.title
        
        # Optional arguments are always provided as key-value pairs
        task = Task('t1', service = 'prman')
        assert task.service == 'prman'
        ## [alf_task_init]
        
        ## [alf_task_impclit_cmd]
        assert len(task.cmds) == 0
        task.cmds.append(('executable', '-arg', '-foo'))
        assert len(task.cmds) == 1 and task.cmds[0].args[0] == '-arg'
        
        # this is similar, but more explicit
        task.cmds.append(Cmd('foo'))
        assert task.cmds[-1].executable == 'foo'
        
        # When specifying a single command, it works in any way
        task = Task('t2', cmds = 'foo')
        assert task.cmds[0].executable == 'foo'
        
        # With multiple, you have to be more specific
        task = Task('t2', cmds = (
                                   Cmd('foo'),
                                   Cmd('bar')
                               )
                )
        assert len(task.cmds) == 2
        
        # Subtasks can be added similarly
        t3 = task.subtasks.append('t3')
        assert t3.title == 't3'
        
        # or durign initialization
        task = Task('new', subtasks = (
                                            Task('sub1'),
                                            Task('sub2'),
                                      )
                   )
        
        assert len(task.subtasks) == 2
        ## [alf_task_impclit_cmd]
        
        
    def test_complex_example(self):
        """some more """
        
        ## [alf_example_complex]
        
        job = Job(  title='job',
                    after=JobDate(  month=6, 
                                    day=23, 
                                    hour=13, 
                                    minute=45 ),
                    init = Assignments(
                                        root_path='root', 
                                        otherval='this'
                                      ),
                    cleanup = Cmd('foo -f file'.split(), service='prman', tags='nuke', id='clean'),
                    subtasks = ( 
                                Task('t1',
                                    cmds=Cmd('foo', '-bar'),
                                    subtasks=(  # Utilty types are auto-created
                                        Task(   't3',
                                                cmds=( 
                                                        Cmd('foo', '-bar'),
                                                        Cmd('hello', 'world',
                                                            refersto = 'maintask') 
                                                   ),
                                                subtasks=Instance('t2')
                                            )
                                        ),
                                    id='maintask'# end t1 subtasks 
                                ),# end t1
                                Task('t2')
                    ), # end job tasks
                    atleast=5,
                    atmost=10,
                    tags = ('foo', 'FOo'),
                    service = 'prman',
                    envkey = 'environ',
                    comment = """hello there"""
        )# end job
        
        ## [alf_example_complex]
        
        ## [alf_serialize]
        AlfSerializer().init(sys.stdout).serialize(job)
        ## [alf_serialize]
        
        """
## [alf_serialize_output]
Job -after { 6 23 13:45 } -atleast 5 -atmost 10 -comment { hello there } -envkey environ -service prman -tags foo -title job -cleanup {
    Cmd { foo -f file } -id clean -service prman -tags nuke 
} -init {
    Assign otherval this 
    Assign root_path root 
} -subtasks {
    Task t1 -id maintask -cmds {
        Cmd { foo -bar } 
    } -subtasks {
        Task t3 -cmds {
            Cmd { foo -bar } 
            Cmd { hello world } -refersto maintask 
        } -subtasks {
            Instance t2 
        } 
    } 
    Task t2 
}
        ## [alf_serialize_output]
        """
        
    def test_runtime_adjustments(self):
        """change things at runtime with full type checking"""
        ## [alf_dynamic_modifications]
        job = Job()
        job.title = 'job'
        
        for tid in range(3):
            task = job.subtasks.append(Task("t%i" % tid,
                                         cmds = Cmd('executable%i' % tid))
                                    )
            for stid in range(2):
                task.subtasks.append("t%ist%i" % (tid, stid)).cmds.append('subexecutable%i' % stid)
            # end for each sub task id
        # end for each task to create
        
        job.service = 'prman'
        ## [alf_dynamic_modifications]
        
        AlfSerializer().init(sys.stdout).serialize(job)
        
        """
        ## [alf_dynamic_modifications_result]
Job -service prman -title job -subtasks {
	Task t0 -cmds {
		Cmd executable0 
	} -subtasks {
		Task t0st0 -cmds {
			Cmd subexecutable0 
		} 
		Task t0st1 -cmds {
			Cmd subexecutable1 
		} 
	} 
	Task t1 -cmds {
		Cmd executable1 
	} -subtasks {
		Task t1st0 -cmds {
			Cmd subexecutable0 
		} 
		Task t1st1 -cmds {
			Cmd subexecutable1 
		} 
	} 
	Task t2 -cmds {
		Cmd executable2 
	} -subtasks {
		Task t2st0 -cmds {
			Cmd subexecutable0 
		} 
		Task t2st1 -cmds {
			Cmd subexecutable1 
		} 
	} 
} 
        ## [alf_dynamic_modifications_result]
        """
        
        
    def test_cmd(self):
        """show cmd syntax"""
        
        ## [alf_cmd]
        # Create a command with a single space separated flag string
        cmd = Cmd('executable', '-foo -bar -file %s' % 'file.ext')
        # Access the executable trough the documented name, appname, or our alias, executable
        assert cmd.executable == cmd.appname == 'executable', "executable is an alias for appname"
        
        # The attribute name for flags is args, which is a list of strings
        assert len(cmd.args) == 1
        
        cmd = Cmd('foo', '-baz', '-bar=1', '-val', 'arg')
        assert len(cmd.args) == 4
        ## [alf_cmd]
        
        
    def test_job_date(self):
        """job date usage"""
        ## [alf_jobdate_usage]
        # A job that launches after 23rd of June, 14:30
        job = Job(after=(6, 23, 14, 30))
        
        # Auto-conversion to a Date
        assert isinstance(job.after, JobDate)
        assert job.after.month == 6
        assert job.after.day == 23
        
        # You can also write it more explicitly, which is probably easier to understand
        job.after = JobDate(day=5, month=3, hour=14, minute=20)
        ## [alf_jobdate_usage]
        
    def test_tags(self):
        ## [alf_tags]
        job = Job(tags=('nuke', 'Nuke', 'linux'))
        assert len(job.tags) == 2 and job.tags[0] == 'nuke'
        
        job.tags.append('NUKE')
        assert len(job.tags) == 2
        ## [alf_tags]
        
    def test_assignments(self):
        """Assignment syntax"""
        
        ## [alf_assignments]
        # non-strings will be converted to strings when needed
        # This form de-duplicates variable names natively
        job = Job(init=Assignments(var1=14, var2='hello'))
        assert len(job.init) == 2 
        ## [alf_assignments]
        
        ## [alf_assignments_explicit]
        job = Job(init=(
                            Assign('var1', 14),
                            Assign('var2', 'hello')
                       )
                )
        
        # This is similar
        job = Job(init=Assignments(
                                        ('var', 'hi'), 
                                        Assign('var2', 'ho')
                                  )
                )
        ## [alf_assignments_explicit]
        
        ## [alf_assignments_duplicates]
        # 'var' already exists in assignments
        self.failUnlessRaises(AssertionError, job.init.append, ('var', 'ho'))
        ## [alf_assignments_duplicates]
    

# end class TractorAlfTests
