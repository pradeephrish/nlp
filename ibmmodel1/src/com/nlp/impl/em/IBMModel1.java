package com.nlp.impl.em;

import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;

public class IBMModel1 {
	public static void main(String[] args) {
		
		if(args.length==0){
			System.out.println("Please provide input arguments... ");
			
			System.exit(0);
		}
		
		
		IBMModel1 ibmModel1 = new IBMModel1();
		List<String> sentences = readFile(args[1]); //english corpo
		ibmModel1.setEnglishSentences(sentences);
		sentences = readFile(args[2]); //english corpo
		ibmModel1.setGermanSentences(sentences);
		//call for all sentences
		for (int i = 0; i < sentences.size(); i++) {
			//initialize 
			ibmModel1.initializeAndCompute(ibmModel1.germanSentences.get(i), ibmModel1.englishSentences.get(i));
		}
		ibmModel1.model1EM(10); // 10 steps
		
	}

	private List<String> germanSentences;
	private List<String> englishSentences;
	private Map<String,Double> mapT; // t(f|e) - score
	
	
	public static List<String> readFile(String fileName){
		List<String> lines = new ArrayList<String>();
		try{
			BufferedReader br = new BufferedReader(new FileReader(fileName));
			String line;
			while ((line = br.readLine()) != null) {
			   lines.add(line);
			}
			br.close();
		}catch(Exception e){
			System.out.println("Please check file name arguments (Location of file should be correct)");
		}
		return lines;
	}
	

	private void model1EM(Integer steps){
		Map<String,Double> mapC; // count(f|e) score - set to 0 at each EM iteration 
		
		mapC= setCountstoZero();
		setTotaltoZero();  //doesn't neet to return ,sets global totals object scores to zero
		for (int i = 0; i < getGermanSentences().size(); i++) { //german or english sentencs ,jsut need size
			String germanWords[] = getGermanSentences().get(i).split(" ");
			String englishWords[]=  getEnglishSentences().get(i).split(" ");
			int[] total_s = new int[germanWords.length];
			for (int j = 0; j < germanWords.length; j++) {
					for (int k = 0; k < englishWords.length; k++) {
						total_s[j]+=mapT.get(germanWords[j]+"-"+englishWords[k]);
					}
			}
			for (int j = 0; j < germanWords.length; j++) {
				for (int k = 0; k < englishWords.length; k++) {
					Double value = mapC.get(germanWords[j]+"-"+englishWords[k]);
					value+=mapT.get(germanWords[j]+"-"+englishWords[k]) / total_s[j];
					mapC.put(germanWords[j]+"-"+englishWords[k], value); //update value
					Double tValue = mapTotal.get(englishWords[k]);
					tValue+=mapT.get(germanWords[j]+"-"+englishWords[k]) / total_s[j];
					mapTotal.put(englishWords[k], tValue); //update totalValue
				}
			}
			 //for all e 
			//   for all f
			//      update t(f|e)
			Iterator<Entry<String, Double>> iterator = mapT.entrySet().iterator();
			while(iterator.hasNext()){
				Entry<String, Double> entry = iterator.next();
				String totalKey  = entry.getKey().substring(entry.getKey().indexOf("-")+1);
				Double updatedValue = mapC.get(entry.getKey())/mapTotal.get(totalKey);
			}
		}
		
	}
	
	
	
	
	
	private void setTotaltoZero() {
		// TODO Auto-generated method stub
		
		if(mapTotal.size()==0)
		{
			System.out.println("Map total is empty, Please intialize !");
			return ;
		}
		Iterator<Entry<String, Double>> iterator = mapTotal.entrySet().iterator();
		while(iterator.hasNext())
			iterator.next().setValue(0.0); //setting to zero
	}





	private Map<String, Double> setCountstoZero() {
		// TODO Auto-generated method stub
		if(mapT.size()==0){
			System.out.println("Please initialize mapT first");
			return null;
		}	
		HashMap<String,Double> mapC = new HashMap<String,Double>();
		Iterator<Entry<String, Double>> iterator = mapT.entrySet().iterator();
		while(iterator.hasNext()){
			Entry<String, Double> entry = iterator.next();
			mapC.put(entry.getKey(), 0.0); //setting to zero
		}
		return mapC;
	}



 

	/*
	 * Map<String> shows t(e|t) eg he|तो -->(is stored into string as) he-तो
	 */
	public void initializeAndCompute(String german,
			String english) {

		String[] words1 = german.split(" ");
		String[] words2 = english.split(" ");

		for (int i = 0; i < words1.length; i++) {
			for (int j = 0; j < words2.length; j++) {
				String key = words1 + "-" + words2;
				if (!mapT.containsKey(key))
					mapT.put(key, getInitialAtomic(words1[i], words2[j]));
			}
		}
	}

	/*
	 * In the initialization step, you should set T(f|e) = 1/n(e) where n(e)
	 * is the number of different German words seen in German sentences aligned
	 * to English sentences that contain the word e. This ensures that the
	 * conditional T(f|e) probabilities sum to 1.
	 */
	
	Map<String,Double> mapTotal; // total(e) score  - set to 9 at each EM iteration 
	
	private Double getInitialAtomic(String germanWord, String englishWord) {
		
		mapTotal.put(englishWord, 0.0); //this will be used later
		
		// TODO Auto-generated method stub
		List<String> germanSentences = getGermanSetences(); 
	    List<String> englishSentences = getEnglishSetences();
	    
	    if(germanSentences.size()!=englishSentences.size()){
	    	System.out.println("Something wrong ! size doesn't match");
	    	return null;
	    }
	    
	    Double count=0.0;
	    Set<String> germanwords = new HashSet<String>();
	    for (int i = 0; i < germanSentences.size(); i++) {
			if(englishSentences.get(i).contains(englishWord)){
				Integer index = getIndex(englishSentences.get(i),englishWord);
				String germanW = germanSentences.get(i).split(" ")[index];
				if(!germanwords.contains(germanW)) // if it's different then only count
					++count;
			}
		}
	    
	    
		return count;
	}

	private Integer getIndex(String string, String englishWord) {
		// TODO Auto-generated method stub
		String words[] = string.split(" ");
		for (int i = 0; i < words.length; i++) {
			if(words[i].equalsIgnoreCase(englishWord)) //note equal ingnore case
				return i;
		}
		return null;
	}

	private List<String> getEnglishSetences() {
		// TODO Auto-generated method stub
		return getGermanSentences();
	}

	private List<String> getGermanSetences() {
		// TODO Auto-generated method stub
		return getEnglishSentences();
	}





	public List<String> getGermanSentences() {
		return germanSentences;
	}





	public void setGermanSentences(List<String> germanSentences) {
		this.germanSentences = germanSentences;
	}





	public List<String> getEnglishSentences() {
		return englishSentences;
	}





	public void setEnglishSentences(List<String> englishSentences) {
		this.englishSentences = englishSentences;
	}

}
