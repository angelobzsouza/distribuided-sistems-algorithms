all:
	javac UploadFile.java Server.java Client.java

clean:
	rm *.class

create-files:
	dd if=/dev/zero of=1Gb.txt count=1024 bs=1024000
	dd if=/dev/zero of=100Mb.txt count=1024 bs=102400
	dd if=/dev/zero of=5Mb.txt count=1024 bs=5120
	dd if=/dev/zero of=1Mb.txt count=1024 bs=1024

create-folder:
	mkdir uploadedFiles