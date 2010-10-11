all:
	@echo 'Uso: make <opt>'
	@echo opcoes: gui resources

gui: clientmain.ui
	pyuic4 -x clientmain.ui -o guiPyQt4.py

resources: images.qrc
	pyrcc4 -o images_rc.py
