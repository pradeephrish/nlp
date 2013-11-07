package com.nlp.impl.em;

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;

public class SerializeData {
	
	
	public static void serialize(String outputFileName,Object object) throws IOException{
		FileOutputStream fileOutputStream = new FileOutputStream(outputFileName);
		ObjectOutputStream objectOutputStream  = new ObjectOutputStream(fileOutputStream);
		objectOutputStream.writeObject(object);
	}
	
	
	
	public  static Object deserialize(String inputFileName) throws ClassNotFoundException, IOException{
		FileInputStream fileInputStream = new FileInputStream(inputFileName);
		ObjectInputStream objectInputStream = new ObjectInputStream(fileInputStream);
		
		return objectInputStream.readObject();
	
	
	}
	
	
	public static void main(String[] args){
//			List<List<Map<String, List<Double>>>> dictionary = (List<List<Map<String, List<Double>>>>) deserialize("object/test.obj");
//			serialize("data/test.obj", map);
	}
	
}
