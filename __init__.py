# -*- coding: utf-8 -*-
class Depand:
    def __init__(self,relydict={}):
        self.relys={}
        for k,v in relydict.items():
            self.addrelys(k,v)
    def addrelys(self,keys,relys):
        keys,relys=self._tokey(keys),self._tokey(relys)
        for k in keys+relys:
            if k not in self.relys:
                self.relys[k]=[]
        for key in keys:
            self.relys[key]=self._tokey(self.relys[key]+relys)
            try:
                self.relys[key].remove(key)
            except:
                pass
    def delrelys(self,keys,relys):
        keys=list(self._eles(keys))
        relys=list(self._eles(relys))
        for key in keys:
            for rely in relys:
                try:
                    self.relys[key].remove(rely)
                except:
                    pass
    def ifrely(self,keys,relys):
        keys,relys=self._tokey(keys),self._tokey(relys)
        result=[]
        for k in keys:
            temp=self._ifrely(k,relys,[])
            if temp is None:
                return None
            result+=temp
        return self._tokey(result)
    def decomp(self):
        return self.decompBC()
    def decompBC(self):
        comps=[[self._tokey(self.relys.keys()),[]]]
        funcs=[self._key2key,
             self._key2other,
             self._other2key,
             self._other2other,
             ]
        while(1):
            comps2=self._decomp(comps,funcs)
            if comps2==comps:
                return comps
            comps=comps2
        return comps
    def decomp1(self):
        comps=[[self._tokey(self.relys.keys()),[]]]
        funcs=[self._key2key,
             ]
        while(1):
            comps2=self._decomp(comps,funcs)
            if comps2==comps:
                return comps
            comps=comps2
        return comps
    def decomp2(self):
        comps=[[self._tokey(self.relys.keys()),[]]]
        funcs=[self._key2key,
             self._other2key,
             ]
        while(1):
            comps2=self._decomp(comps,funcs)
            if comps2==comps:
                return comps
            comps=comps2
        return comps
    def decomp3(self):
        comps=[[self._tokey(self.relys.keys()),[]]]
        funcs=[self._key2key,
             self._other2key,
             self._other2other,
             ]
        while(1):
            comps2=self._decomp(comps,funcs)
            if comps2==comps:
                return comps
            comps=comps2
        return comps
    def _decomp(self,comps,funcs):
        comps=list(comps)
        idx=0
        while(idx<len(comps)):
            for func in funcs:
                temps=func(comps[idx])
                comps[idx:idx+1]=temps
            idx+=1
        comps=self._compComps(comps)
        return comps
    def _other2key(self,comp):
        keys,others=list(comp[0]),list(comp[1])
        comps=[]
        for ot in list(others):
            temp=self.ifrely(ot,keys)
            if temp is None or len(temp)==0:
                comps.append([[ot],[]])
                others.remove(ot)
            elif len(temp)<len(keys):
                comps.append([temp,[ot]])
                others.remove(ot)
        comps.append([keys,others])
        comps=self._compComps(comps)
        return comps
    def _key2key(self,comp):
        keys,others=list(comp[0]),list(comp[1])
        comps=[]
        for key in list(keys):
            temp=[k for k in keys if k!=key]
            temp=self.ifrely(key,temp)
            if temp is not None and len(temp)>0:
                comps.append([temp,[key]])
                keys.remove(key)
        comps.append([keys,others])
        comps=self._compComps(comps)
        return comps
    def _key2other(self,comp):
        keys,others=list(comp[0]),list(comp[1])
        comps=[]
        for key in list(keys):
            temp=self.ifrely(key,others)
            if temp is not None and len(temp)>0:
                if self.ifrely(temp,key) is None:
                    comps.append([temp,[key]])
                    keys.remove(key)
                    keys+=temp
                    for t in temp:
                        others.remove(temp)
        comps.append([keys,others])
        comps=self._compComps(comps)
        return comps
    def _other2other(self,comp):
        keys,others=list(comp[0]),list(comp[1])
        if len(others)<=1:
            return [comp]
        comps=[]
        for ot in list(others):
            temp=[o for o in others if o!=ot]
            temp=self.ifrely(ot,temp)
            if temp is not None and len(temp)>0:
                comps.append([temp,[ot]])
                others.remove(ot)
        comps.append([keys,others])
        comps=self._compComps(comps)
        return comps
    def _tokey(self,key):
        return list(sorted(set(self._eles(key))))
    def _compComps(self,comps):
        comps2={}
        for ks,os in comps:
            ks,os=tuple(self._tokey(ks)),self._tokey(os)
            try:
                comps2[ks]+=os
            except:
                comps2[ks]=os
        try:
            del comps2[tuple([])]
        except:
            pass
        return [[list(k),self._tokey(v)] for k,v in comps2.items()]
    def _ifrely(self,key,relys,last):
        if key in relys:
            return [key]
        if key in last:
            return []
        last.append(key)
        result=[]
        origins=self.relys[key]
        if len(origins)==0:
            return None
        result=[]
        for ori in origins:
            r=self._ifrely(ori,relys,last)
            if r is None:
                return None
            result+=r
        return self._tokey(result)
    def _eles(self,data):
        if isinstance(data,str):
            yield data
            return
        try:
            for d in data:
                for e in self._eles(d):
                    yield e
        except:
            yield str(data)