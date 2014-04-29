package com.jd.bdp.nlp.loc;

import java.util.PriorityQueue;

/**
 * Created by zhengchen on 14-4-29.
 */
public class Location {

    //private static final String[] locKeywords = {"省","市","区","县","道","镇","乡","村","庙","寺","苑","厦","里","弄","园","路","街","巷"};
    private static final char[] locKeywords = "省市区县道镇乡村庙寺苑厦里弄园路街巷".toCharArray();
    public static final int keyNum = locKeywords.length;
    //private String[] locs = new String[keyNum+1];
    private String loc;

    /**
     * The class store the index of locKeywords and the index of location.
     */
    private class WordIndex implements Comparable<WordIndex>{
        public int word;
        public int index;

        public WordIndex(int w, int i) {
            word = w;
            index = i;
        }

        /**
         * Order by the index of char in location String.
         */
        public int compareTo(WordIndex w) {
            if (this.index < w.index)
                return -1;
            else if (this.index == w.index)
                return 0;
            else
                return 1;
        }

    }

    /**
     *  Contructor that takes a String of location to split
     *
     *  @param loc a String of location to be splited to locs.
     */
    public Location(String loc) {
        this.loc = loc;
    }

    /**
     * Split the location to locs by the locKeywords
     * and put the locs into locs array in the same order with locKeywords.
     *
     * @return An array of Strings represent the structure of location in the order of the keywords.
     */
    public String[] splitLoc() {
        String[] locs = new String[keyNum+1];
        PriorityQueue<WordIndex> wipq = new PriorityQueue<WordIndex>();
        for (int i = 0; i < keyNum; i++) {
            // Do not put the last loc into the wipq at this time.
            for (int j = 0, n = this.loc.length(); j < n-1; j++) {
                // TODO 小区 区 is different, so should change the char matching to string matching.
                if (locKeywords[i] == this.loc.charAt(j)) {
                    // Sorted by the index of char in location.
                    wipq.offer(new WordIndex(i, j));
                    // Once find the equal char, stop the researching.
                    break;
                }
            }
        }
        // Whatever the last loc contains the keywords, it belongs to the locs[keyNum].
        if (wipq.isEmpty()) locs[keyNum] = this.loc;
        else {
            // 0 i1 | i1 i2 | i2 i3 | ... | in-1 in
            WordIndex pwi = wipq.poll();
            locs[pwi.word] = this.loc.substring(0, pwi.index);
            while (!wipq.isEmpty()) {
                WordIndex wi = wipq.poll();
                locs[wi.word] = this.loc.substring(pwi.index, wi.index);
                pwi = wi;
            }
            locs[keyNum] = this.loc.substring(pwi.index);
        }
        return locs;
    }

}
