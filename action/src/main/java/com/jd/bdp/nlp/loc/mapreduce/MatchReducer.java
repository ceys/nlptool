package com.jd.bdp.nlp.loc.mapreduce;

import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.io.Text;

import java.util.ArrayList;
import com.jd.bdp.nlp.loc.*;

/**
 * Created by zhengchen on 14-4-29.
 */
public class MatchReducer extends Reducer<Text, Text, Text, Text> {

    @Override
    public void reduce(Text key, Iterable<Text> values, Context context) {
        // Store the locations of yx.
        ArrayList<String> yxlocs = new ArrayList<String>();
        // Store the index of jd locations.
        Trie[] jdLocArray = new Trie[Location.keyNum+1];
        for (Text comAddr: values) {
            // value : companyid \t location \t uid
            String[] cons = comAddr.toString().split("\t");
            if (cons[0].equals("jd")) {
                for (String s : new Location(cons[1]).splitLoc()) {
                    if (s != null) {

                    }
                }

            } else {
                yxlocs.add(cons[1]);
            }
        }
    }
}
