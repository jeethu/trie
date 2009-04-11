# -*- coding: utf-8 -*-

_SENTINEL = ()

class TST(object) :
    __slots__ = ('splitchar','l','m','r','v')
    def __init__( self, ch=None ) :
        self.splitchar = ch
        self.l = self.m = self.r = None

    def __getstate__( self ) :
        l = [self.splitchar,self.l,self.m,self.r]
        if hasattr(self,'v') :
            l.append(self.v)
        return tuple(l)

    def __setstate__( self, l ) :
        self.splitchar = l[0]
        self.l = l[1]
        self.m = l[2]
        self.r = l[3]
        if len(l) > 4 :
            self.v = l[4]

    @classmethod
    def insert( klass, p, k, v ) :
        ch = k[0]
        if p is None :
            p = TST(ch)
        elif p.splitchar is None :
            p.splitchar = ch
        if ch < p.splitchar :
            p.l = klass.insert( p.l, k, v )
        elif ch == p.splitchar :
            k = k[1:]
            if k :
                p.m = klass.insert(p.m, k, v)
            else :
                p.v = v
        else :
            p.r = klass.insert(p.r, k, v)
        return p

    def add( self, k, v ) :
        return self.insert( self, k, v )

    def search( self, s, fallback=None ) :
        p = self
        while p :
            ch = s[0]
            if ch < p.splitchar :
                p = p.l
            elif ch == p.splitchar :
                s = s[1:]
                if not s :
                    if hasattr(p,'v') :
                        return p.v
                    break
                p = p.m
            else :
                p = p.r
        return fallback

    def prefix_search( self, s ) :
        p = self
        while p :
            ch = s[0]
            if ch < p.splitchar :
                p = p.l
            elif ch == p.splitchar :
                s = s[1:]
                if not s :
                    return list(p)
                p = p.m
            else :
                p = p.r
        return []

    def bulk_add( self, l, start=0, stop=None, sorted=False ) :
        '''
        This structure is insertion order sensitive,
        bulk_add recursively builds the tree in optimal order
        '''
        if not sorted :
            l.sort()
        if stop is None :
            stop = len(l)
        diff = stop - start
        if diff == 1 :
            self.add(l[start][0],l[start][1])
        elif diff == 2 :
            self.add(l[start][0],l[start][1])
            self.add(l[start+1][0],l[start+1][1])
            return
        else :
            mid_p = start + (diff / 2)
            self.add(l[mid_p][0],l[mid_p][1])
            self.bulk_add(l,mid_p+1,stop,True)
            self.bulk_add(l,start,mid_p,True)

    def __contains__( self, k ) :
        if self.search(k,_SENTINEL) is _SENTINEL :
            return False
        return True

    def __iter__(self) :
        stack = []
        p = self
        if not p :
            return
        while True :
            if p.r :
                stack.append(p.r)
            if p.m :
                stack.append(p.m)
            if p.l :
                stack.append(p.l)
            if hasattr(p,'v') :
                yield p.v
            if not stack :
                break
            p = stack.pop()
