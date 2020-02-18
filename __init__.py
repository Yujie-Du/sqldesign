# -*- coding: utf-8 -*-


class Depand:
    def __init__(self):
        self.data={}
    #添加字段依赖关系
    def addrelys(self,keys,relys=[]):
        changed=0
        keys=list(self._eles(keys))
        relys=list(self._eles(relys))
        for key in keys:
            if key not in self.data:
                self.data[key]=_Key(key)
            for rely in relys:
                if rely not in self.data:
                    self.data[rely]=_Key(rely)
                if self.data[key].addrely(self.data[rely]):
                    changed+=1
        return changed
    def delrelys(self,keys,relys=[]):
        changed=0
        keys=list(self._eles(keys))
        relys=list(self._eles(relys))
        relys=[r for r in relys if r in self.data]
        for key in keys:
            if key not in self.data:
                continue
            for rely in relys:
                if self.data[key].delrely(self.data[rely]):
                    changed+=1
        return changed
    def ifrely(self,key,relys):
        key=self.data[key]
        relys=list(self._eles(relys))
        relys=[self.data[r] for r in relys]
        result=key.ifrely(relys)
        if result is None:
            return None
        return [r.key for r in result]
    def getorigins(self):
        relys={}
        for k in self.data.values():
            relys[k.key]=[r.key for r in k.getorigins()]
        return relys
    def getrelys(self):
        relys={}
        for k in self.data.values():
            relys[k.key]=[r.key for r in k.getrelys()]
        return relys
    def decomp(self):
        return self.decomp3()
    def decomp1(self):
        relys=self.getorigins()
        result={}
        for k,v in relys.items():
            if len(v)==0:
                continue
            v=tuple(v)
            if v in result:
                result[v].append(k)
            else:
                result[v]=[k]
        return [[tuple(k),tuple(v)] for k,v in result.items()]
    def decomp2(self):
        relys=self.getrelys()
        result={}
        for k,v in relys.items():
            if len(v)==0:
                continue
            v=tuple(v)
            if v in result:
                result[v].append(k)
            else:
                result[v]=[k]
        return [[tuple(k),tuple(v)] for k,v in result.items()]
    def decomp3(self):
        comps=[]
        for comp in self.decomp2():
            comps+=self._decomp3unit(comp)
        return comps
    def _decomp3unit(self,comp):
        keys=list(comp[1])
        depand=Depand()
        for idx in range(len(keys)):
            key=keys[idx]
            temp=[t for t in keys if t!=key]
            temp=self.ifrely(key,temp)
            if len(temp)>0:
                depand.addrelys(key,temp)
        if len(depand.data)==0:
            return [comp]
        comps2=depand.decomp3()
        for c in comps2:
            for k in c[1]:
                if k in keys:
                    keys.remove(k)
        comp=[comp[0],tuple(keys)]
        comps2.append(comp)
        return comps2
    def _eles(self,data):
        if isinstance(data,str):
            yield data
        else:
            try:
                for d in data:
                    for e in self._eles(d):
                        yield e
            except:
                yield data

class _Key:
    def __init__(self,key):
        self.key=key
        self.origins=[]
        self.relys=[]
        self.dectrely=[]
        self.changed=0
    def ifrely(self,relys,last=[]):
        if self in relys:
            return [self]
        if self in last:
            return []
        last.append(self)
        result=[]
        for ori in self.origins:
            r=ori.ifrely(relys,last)
            if r is None:
                return None
            result+=r
        return result
    def addrely(self,rely):
        if (rely is not self) and (rely not in self.origins):
            self.origins.append(rely)
            self.changed+=1
            return True
        return False
    def delrely(self,rely):
        if rely in self.origins:
            self.origins.remove(rely)
            self.changed+=1
            return True
        return False
    def _addrelys(self,rs):
        tip=False
        for r in rs:
            if self._addrely(r):
                tip=True
        return tip
    def _addrely(self,r):
        if r is self:
            return False
        if r in self.relys:
            return False
        rs=r.getrelys()
        if len(rs)==0:
            self.relys.append(r)
            return True
        return self._addrelys(rs)
    def cleanrelys(self):
        if self.changed>0:
            self.changed=0
            self.relys=[]
            self._addrelys(self.origins)
    def getrelys(self):
        self.cleanrelys()
        return self.relys
    def getorigins(self):
        return self.origins