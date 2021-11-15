//package com.DataStructures.AchintyaSingh;

package lse;

import java.io.*;
import java.util.*;

/**
 * This class builds an index of keywords. Each keyword maps to a set of pages in
 * which it occurs, with frequency of occurrence in each page.
 *
 */
public class LittleSearchEngine {

	/**
	 * This is a hash table of all keywords. The key is the actual keyword, and the associated value is
	 * an array list of all occurrences of the keyword in documents. The array list is maintained in
	 * DESCENDING order of frequencies.
	 */
	HashMap<String,ArrayList<Occurrence>> keywordsIndex;

	/**
	 * The hash set of all noise words.
	 */
	HashSet<String> noiseWords;

	/**
	 * Creates the keyWordsIndex and noiseWords hash tables.
	 */
	public LittleSearchEngine() {
		keywordsIndex = new HashMap<String,ArrayList<Occurrence>>(1000,2.0f);
		noiseWords = new HashSet<String>(100,2.0f);
	}

	/**
	 * Scans a document, and loads all keywords found into a hash table of keyword occurrences
	 * in the document. Uses the getKeyWord method to separate keywords from other words.
	 *
	 * @param docFile Name of the document file to be scanned and loaded
	 * @return Hash table of keywords in the given document, each associated with an Occurrence object
	 * @throws FileNotFoundException If the document file is not found on disk
	 */
	public HashMap<String,Occurrence> loadKeywordsFromDocument(String docFile)
	throws FileNotFoundException
	{
		Scanner keyword = new Scanner(new File(docFile));
		if(docFile == null)
		{
			throw new FileNotFoundException("File Not Found");
		}
		HashMap<String, Occurrence> keyHash = new HashMap<>();
		while(keyword.hasNext())
		{
			String getWord = getKeyword(keyword.next());
			if (getWord != null)
			{
				if(keyHash.containsKey(getWord))
				{
					keyHash.get(getWord).frequency++;
				}
				else
				if(keyHash.containsKey(getWord) == false)
				{
					
					keyHash.put(getWord, new Occurrence(docFile, 1));
				}
			}
		}
		return keyHash;
	}

	/**
	 * Merges the keywords for a single document into the master keywordsIndex
	 * hash table. For each keyword, its Occurrence in the current document
	 * must be inserted in the correct place (according to descending order of
	 * frequency) in the same keyword's Occurrence list in the master hash table.
	 * This is done by calling the insertLastOccurrence method.
	 *
	 * @param kws Keywords hash table for a document
	 */
	public void mergeKeywords(HashMap<String,Occurrence> kws)
	{
		/** COMPLETE THIS METHOD **/
		for (String x : kws.keySet())
		{
			if(keywordsIndex.containsKey(x) == false)
			{
				ArrayList<Occurrence> newList = new ArrayList<>();
				newList.add(kws.get(x));
				keywordsIndex.put(x, newList);
			}
			else
			{
				keywordsIndex.get(x).add(kws.get(x));
				insertLastOccurrence(keywordsIndex.get(x));
			}
		}
	}

	/**
	 * Given a word, returns it as a keyword if it passes the keyword test,
	 * otherwise returns null. A keyword is any word that, after being stripped of any
	 * trailing punctuation(s), consists only of alphabetic letters, and is not
	 * a noise word. All words are treated in a case-INsensitive manner.
	 *
	 * Punctuation characters are the following: '.', ',', '?', ':', ';' and '!'
	 * NO OTHER CHARACTER SHOULD COUNT AS PUNCTUATION
	 *
	 * If a word has multiple trailing punctuation characters, they must all be stripped
	 * So "word!!" will become "word", and "word?!?!" will also become "word"
	 *
	 * See assignment description for examples
	 *
	 * @param word Candidate word
	 * @return Keyword (word without trailing punctuation, LOWER CASE)
	 */
	public String getKeyword(String word)
	{
		/** COMPLETE THIS METHOD **/
		word = word.toLowerCase();
		for(int i = word.length() - 1; i >= 0; i--)
		{
			//. , : ; ? !
			if(!(word.charAt(i)=='.') && !(word.charAt(i)==',') && !(word.charAt(i)==':') && !(word.charAt(i)==';') && !(word.charAt(i)=='?') && !(word.charAt(i)=='!'))
			{
				break;
			}
			else
			{
				word = word.substring(0, i);
			}
		}
		if(noiseWords.contains(word))
		{
			return null;
		}
		for(int i = word.length() - 1; i >= 0; i--)
		{
			if(Character.isLetter(word.charAt(i)) == false)
			{
				return null;
			}
		}
		return word;
	}

	/**
	 * Inserts the last occurrence in the parameter list in the correct position in the
	 * list, based on ordering occurrences on descending frequencies. The elements
	 * 0..n-2 in the list are already in the correct order. Insertion is done by
	 * first finding the correct spot using binary search, then inserting at that spot.
	 *
	 * @param occs List of Occurrences
	 * @return Sequence of mid point indexes in the input list checked by the binary search process,
	 *         null if the size of the input list is 1. This returned array list is only used to test
	 *         your code - it is not used elsewhere in the program.
	 */
	public ArrayList<Integer> insertLastOccurrence(ArrayList<Occurrence> occs)
	{
		/** COMPLETE THIS METHOD **/
		if(occs.size() == 1)
		{
			return null;
		}
		Occurrence occurrence = occs.get(occs.size() - 1);
		ArrayList<Integer> midpoints = new ArrayList<>();
		int base = 0;
		int high = occs.size() - 2;
		int mid = (base + high) / 2;
		while (base <= high)
		{
			mid = (base + high)/2;
			midpoints.add(mid);
			if(occurrence.frequency > occs.get(mid).frequency)
			{
				high = mid - 1;
			}
			else
			if (occurrence.frequency < occs.get(mid).frequency)
			{
				base = mid + 1;
			}
			else
			if (occs.get(mid).frequency == occurrence.frequency)
			{
				break;
			}
		}
		occs.add(mid + 1, occs.remove(occs.size() - 1));
		if (high < base)
		{
			occs.add(base,occs.remove(occs.size() - 1));
		}

		return midpoints;
	}

	/**
	 * This method indexes all keywords found in all the input documents. When this
	 * method is done, the keywordsIndex hash table will be filled with all keywords,
	 * each of which is associated with an array list of Occurrence objects, arranged
	 * in decreasing frequencies of occurrence.
	 *
	 * @param docsFile Name of file that has a list of all the document file names, one name per line
	 * @param noiseWordsFile Name of file that has a list of noise words, one noise word per line
	 * @throws FileNotFoundException If there is a problem locating any of the input files on disk
	 */
	public void makeIndex(String docsFile, String noiseWordsFile)
	throws FileNotFoundException
	{
		Scanner scanLine = new Scanner(new File(noiseWordsFile));
		while (scanLine.hasNext())
		{
			String word = scanLine.next();
			noiseWords.add(word);
		}
		scanLine = new Scanner(new File(docsFile));
		while (scanLine.hasNext())
		{
			String docFile = scanLine.next();
			HashMap<String,Occurrence> kws = loadKeywordsFromDocument(docFile);
			mergeKeywords(kws);
		}
		scanLine.close();
	}

	/**
	 * Search result for "kw1 or kw2". A document is in the result set if kw1 or kw2 occurs in that
	 * document. Result set is arranged in descending order of document frequencies.
	 *
	 * Note that a matching document will only appear once in the result.
	 *
	 * Ties in frequency values are broken in favor of the first keyword.
	 * That is, if kw1 is in doc1 with frequency f1, and kw2 is in doc2 also with the same
	 * frequency f1, then doc1 will take precedence over doc2 in the result.
	 *
	 * The result set is limited to 5 entries. If there are no matches at all, result is null.
	 *
	 * See assignment description for examples
	 *
	 * @param kw1 First keyword
	 * @param kw1 Second keyword
	 * @return List of documents in which either kw1 or kw2 occurs, arranged in descending order of
	 *         frequencies. The result size is limited to 5 documents. If there are no matches,
	 *         returns null or empty array list.
	 */
	public ArrayList<String> top5search(String kw1, String kw2)
	{
		/** COMPLETE THIS METHOD **/
		kw1 = kw1.toLowerCase();
		kw2 = kw2.toLowerCase();
		ArrayList<String> list5 = new ArrayList<String>();
		ArrayList<Occurrence> occurrence1 = keywordsIndex.get(kw1);
		ArrayList<Occurrence> occurrence2 = keywordsIndex.get(kw2);
		if((keywordsIndex.isEmpty()) || (kw1 == null && kw2 == null) || (keywordsIndex.containsKey(kw1) == false && keywordsIndex.containsKey(kw2) == false))
		{
			return null;
		}
		else
		if(keywordsIndex.containsKey(kw1) && (keywordsIndex.containsKey(kw2) == false))
		{
			for(int i = 0; i < occurrence1.size(); i++)
			{
				Occurrence temp = occurrence1.get(i);
				if(list5.size() < 5)
				{
					list5.add(temp.document);
				}
			}
			return list5;
		}
		else
		if((keywordsIndex.containsKey(kw1) == false) && (keywordsIndex.containsKey(kw2)))
		{
			for(int i = 0; i < occurrence2.size(); i++)
			{
				Occurrence temp = occurrence2.get(i);
				if(list5.size() < 5)
				{
					list5.add(temp.document);
				}
			}
			return list5;
		}
		else
		{
			ArrayList<Occurrence> list = new ArrayList<>();
			list.addAll(keywordsIndex.get(kw1));
			list.addAll(keywordsIndex.get(kw2));
			for(int i = 0; i < 5 && list.isEmpty() == false; i++)
			{
				int current = 0;
				int temp = -1;
				for(current = 0; current < list.size() && list.get(current) != null; current++)
				{
					if (list.get(current).frequency == list.get(temp).frequency)
					{
						if(keywordsIndex.get(kw1).contains(list.get(current)))
						{
							if(!list5.contains(list.get(current).document))
							{
								temp = current;
							}
						}
					}
					else
					if (list.get(current).frequency > list.get(temp).frequency)
					{
						if(list5.contains(list.get(current).document) == false)
						{
							temp = current;
						}
					}
					else
					if (temp == -1)
					{
						if (list5.contains(list.get(current).document) == false)
						{
							temp = current;
						}
					}
				}
				if (temp != -1)
				{
					list5.add(list.remove(temp).document);
				}
			}
			return list5;
		}
	}
}