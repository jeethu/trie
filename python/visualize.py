import trie
import tst
from optparse import OptionParser
from gvgen import GvGen

def visualize_tst( t, add_legend=False ) :
    def walk( n ) :
        node = graph.newItem(n.splitchar)
        if n.l :
            graph.styleApply("leftNode",graph.newLink(node,walk(n.l)))
        if n.m :
            graph.styleApply("middleNode", graph.newLink(node,walk(n.m)))
        if n.r :
            graph.styleApply("rightNode", graph.newLink(node,walk(n.r)))
        return node
    if add_legend :
        graph = GvGen('Ternary Search Tree')
    else :
        graph = GvGen()
    graph.styleAppend("leftNode", "color", "blue")
    graph.styleAppend("middleNode", "color", "green")
    graph.styleAppend("rightNode", "color", "red")
    if add_legend :
        graph.legendAppend("leftNode", "Left Node")
        graph.legendAppend("middleNode", "Middle Node")
        graph.legendAppend("rightNode", "Right Node")
    walk( t )
    graph.dot()

def visualize_trie( t ) :
    def walk( node, parent=None ) :
        if parent is None :
            parent = graph.newItem('root')
        for k, v in node[1].items() :
            n = graph.newItem(k)
            graph.newLink(parent, n)
            if v[1] :
                walk(v, n)
    graph = GvGen()
    walk(t.root)
    graph.dot()

def generate_dataset() :
    return [
        ('apple',None),
        ('apricot',None),
        ('grapes',None),
        ('grapefruit',None),
        ('kiwi',None),
        ('banana',None),
        ('peach',None),
        ('pear',None)
    ]

def make_trie( l ) :
    t = trie.Trie()
    for k,v in l :
        t.add(k,v)
    return t

def make_tst( l ) :
    t = tst.TST()
    t.bulk_add(l)
    return t

def main() :
    parser = OptionParser()
    parser.add_option("--trie", dest="type", action="store_const",
                      default=None, const="trie", help="Trie")
    parser.add_option("--tst", dest="type", action="store_const",
                      const="tst", help="Ternary Search Tree")
    (options, args) = parser.parse_args()
    if not options.type :
        parser.print_help()
    else :
        l = generate_dataset()
        if options.type == 'trie' :
            t = make_trie(l)
            visualize_trie(t)
        elif options.type == 'tst' :
            t = make_tst(l)
            visualize_tst(t)

if __name__ == '__main__' :
    main()
