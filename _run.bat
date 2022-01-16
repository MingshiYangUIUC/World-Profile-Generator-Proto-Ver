@ECHO OFF

for /l %%x in (16, 1, 16) do (
	ECHO "Start a render..."
	ECHO %%x
	
	:: start server in another shell so it can be "stopped" by command
	start /B "" _server.bat

	:: wait for server to generate world and "stop" it, adjust this delay (sec) based on device performance
	timeout 70
	taskkill /F /im java.exe
	
	:: call the overviewer            ########################################## CHANGE THESE BELOW ##########################################
	cd Minecraft-Overviewer-master
	build\scripts-3.7\overviewer.py C:\Users\yangm\AppData\Roaming\.minecraft\Server\world C:\Users\yangm\AppData\Roaming\.minecraft\Server\Out

	:: go back 
	cd..

	::	and save some files generated by modified overviewer
	move Out\hdimage.png saved\hdimage%%x.png
	move Out\worldsummary.txt saved\worldsummary%%x.txt
	move Out\worldrarity.txt saved\worldrarity%%x.txt
	move Out\worldfeatures.txt saved\worldfeatures%%x.txt

	::	below saves some output of default overviewer, and png-it can be used to generate hd image using items in this folder
	::move Out\world-lighting saved\world-lighting%%x

	:: delete world files and overviewer output files
	_save_delete.bat
	:: generate final image
	TextOverlay\main.py %%x
	
	ECHO "Saved world data and deleted temporary data, end this render..."
)