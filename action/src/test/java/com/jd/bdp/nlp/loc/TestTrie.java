package com.jd.bdp.nlp.loc;

import org.junit.*;
import static junit.framework.Assert.*;

/**
 * Created by zhengchen on 14-4-28.
 */
public class TestTrie {

    @Test
    public void testContains() {
        Trie t = new Trie();
        t.add("西平庄");
        t.add("海淀西平庄");
        assertEquals(t.contains("大望路"), false);
        assertEquals(t.contains("西平庄"), true);
    }

    @Test
    public void testLeftContains() {
        Trie t = new Trie();
        t.add("西平庄");
        t.add("海淀西平庄");
        assertEquals(t.leftContains("大望路"), false);
        assertEquals(t.leftContains("西平"), true);
        assertEquals(t.leftContains("西平路"), false);
    }


}
