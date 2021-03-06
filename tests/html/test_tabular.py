from tests.html import TestParseHtml
from libextract.html.tabular import children_counter, \
        get_node_counter_pairs, node_counter_argmax, \
        sort_best_pairs, filter_tags


class TestChildrenCounter(TestParseHtml):
    def runTest(self):
        article = self.etree.xpath('//body/article')[0]
        counter = children_counter(article)

        assert len(counter) == 1
        assert counter['div'] == 9


class TestGetNodeCounterPairs(TestParseHtml):
    def setUp(self):
        TestParseHtml.setUp(self)
        self.pairs = get_node_counter_pairs(self.etree)

    def runTest(self):
        u = {elem.tag: counter for elem, counter in self.pairs}
        u.pop('head')
        assert u == {
            'article': {'div': 9},
            'body': {'article': 1, 'footer': 1},
            'html': {'body': 1, 'head': 1},
            }


class TestSortBestPairs(TestGetNodeCounterPairs):
    def setUp(self):
        TestGetNodeCounterPairs.setUp(self)
        self.article = self.etree.xpath('//body/article')[0]
        self.sorted_pairs = sort_best_pairs(node_counter_argmax(self.pairs),
                                            limit=1)

    def runTest(self):
        assert self.sorted_pairs == [
            (self.article, [('div', 9)])
            ]


class TestFilterTags(TestSortBestPairs):
    def runTest(self):
        u = list(filter_tags(self.sorted_pairs))
        assert u == [self.article]

        for child in self.article:
            assert child.tag == 'div'
