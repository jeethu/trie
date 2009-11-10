(function() {
    function Trie() {
        this.root = [null, {}];
    }

    Trie.prototype.add = function( key, value ) {
        var node, ch, curr_node = this.root;
        for(var i=0,k_len=key.length;i<k_len;i++) {
            ch = key.charAt(i);
            node = curr_node[1];
            if(ch in node) {
                curr_node = node[ch];
            } else {
                curr_node = node[ch] = [null,{}];
            }
        }
        curr_node[0] = value;
    };

    Trie.prototype.find = function( key ) {
        var ch, curr_node = this.root;
        for(var i=0,k_len=key.length; i<k_len; i++) {
            ch = key.charAt(i);
            if(ch in curr_node[1]) {
                curr_node = curr_node[1][ch];
            } else {
                return;
            }
        }
        return curr_node[0];
    };

    Trie.prototype.find_prefix = function( key ) {
        var ch, curr_node = this.root;
        var remainder = key;
        for(var i=0,k_len=key.length;i<k_len;i++) {
            ch = key.charAt(i);
            if(ch in curr_node[1]) {
                curr_node = curr_node[1][ch];
            } else {
                return [curr_node[0], remainder];
            }
            remainder = remainder.slice(1,remainder.length);
        }
        return [curr_node[0], remainder];
    };

    function _find_prefix_match( trie, key ) {
        var ch, curr_node = trie.root;
        var remainder = key;
        for(var i=0,k_len=key.length;i<k_len; i++) {
            ch = key.charAt(i);
            if(ch in curr_node[1]) {
                curr_node = curr_node[1][ch];
            } else {
                break;
            }
            remainder = remainder.slice(1,remainder.length);
        }
        return [curr_node,remainder];
    }

    Trie.prototype.find_prefix_matches = function( key ) {
        var l = _find_prefix_match( this, key );
        if(l[1].length>0) {
            return [];
        }
        var d, stack = [l[0]], ret = [];
        while(stack.length>0) {
            d = stack.pop();
            if(d[0]) {
                ret.unshift(d[0]);
            }
            for(var c in d[1]) {
                if(d[1].hasOwnProperty(c)) {
                    stack.push(d[1][c]);
                }
            }
        }
        return ret;
    };
    window['Trie'] = Trie;
}());
