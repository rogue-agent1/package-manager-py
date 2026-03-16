from collections import defaultdict,deque
class Package:
    def __init__(self,name,version,deps=None):
        self.name=name;self.version=version;self.deps=deps or []
    def __repr__(self): return f"{self.name}@{self.version}"
class Registry:
    def __init__(self): self.packages=defaultdict(list)
    def publish(self,pkg): self.packages[pkg.name].append(pkg)
    def resolve(self,name,version=None):
        pkgs=self.packages.get(name,[])
        if not pkgs: raise ValueError(f"Not found: {name}")
        if version: return next((p for p in pkgs if p.version==version),pkgs[-1])
        return pkgs[-1]
class Installer:
    def __init__(self,registry): self.registry=registry; self.installed={}
    def install(self,name,version=None):
        if name in self.installed: return []
        pkg=self.registry.resolve(name,version)
        order=[]; visited=set()
        def resolve(p):
            if p.name in visited: return
            visited.add(p.name)
            for dep_name,dep_ver in p.deps:
                dep=self.registry.resolve(dep_name,dep_ver)
                resolve(dep)
            order.append(p)
        resolve(pkg)
        for p in order: self.installed[p.name]=p
        return order
if __name__=="__main__":
    reg=Registry()
    reg.publish(Package("utils","1.0.0"))
    reg.publish(Package("logger","1.0.0",[("utils","1.0.0")]))
    reg.publish(Package("http","2.0.0",[("logger","1.0.0"),("utils","1.0.0")]))
    reg.publish(Package("app","1.0.0",[("http","2.0.0")]))
    inst=Installer(reg)
    order=inst.install("app")
    names=[p.name for p in order]
    assert names.index("utils")<names.index("logger")<names.index("http")<names.index("app")
    print(f"Install order: {order}")
    print("All tests passed!")
