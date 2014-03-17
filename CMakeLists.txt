
python_project(
		NAME
			btractor
		VERSION
			0.1.0-devel
		AUTHORS
			"Sebastian Thiel <byronimo@gmail.com>"
		ROOT_PACKAGE
			btractor
		PYSIDE_UI_FILES
			btractor/submission/gui/ui/submit.ui
			btractor/submission/gui/ui/mayarender.ui
			btractor/submission/gui/ui/executor.ui
			btractor/submission/gui/ui/mayabatch.ui
			btractor/submission/gui/ui/chunk.ui
			btractor/submission/gui/ui/job.ui
			btractor/submission/gui/ui/multitask.ui
			btractor/submission/gui/ui/message.ui
			btractor/submission/gui/window.ui
			btractor/submission/gui/ctrl_single.ui
		SDKS
			pyside 1.2.1
		SPHINX_CONFIG_IN
			DEFAULT
		DOXYFILE_IN
			DEFAULT
		)
