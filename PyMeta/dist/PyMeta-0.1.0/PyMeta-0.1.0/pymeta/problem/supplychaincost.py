class SupplyChainCostState:
    def __init__(self):
        self.dists=[]
        self.names=['WM','PW','SP']


if __name__ == '__main__':
    dd = SupplyChainCostState()
    print 'printing dd' , vars(dd)
    pp = dd;
    #pp['dists'].append('222')
    pp.dists.append('222')
    print 'printing dd' , vars(dd)