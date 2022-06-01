package org.kivy.sharedstorage;

import java.io.*;

public class StreamCopy {
    public StreamCopy(InputStream inputStream, FileOutputStream outputStream)
	throws IOException {
	int DEFAULT_BUFFER_SIZE = 8192;
	int read;
	byte[] bytes = new byte[DEFAULT_BUFFER_SIZE];
	while ((read = inputStream.read(bytes)) != -1) {
	    outputStream.write(bytes, 0, read);
	}
	outputStream.flush();
	outputStream.close();
    }
}
