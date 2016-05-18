class Banks:
    banks = []
    
    '''
    @param banksList = List[Bank]
    '''
    def __init__(self, banksList):
        self.banks = banksList
    
    def __len__(self):
        return len(self.banks)
    
    def __getitem__(self, index):
        return self.get(index)

    def __delitem__(self, index):
        try:
            del self.banks[index]
        except IndexError:
            raise IndexError("Element not found")

    def get(self, index):
        try:
            return self.banks[index]
        except IndexError:
            raise IndexError("Element not found")
    
    def append(self, bank):
        self.banks.append(bank)
    
    def insert(self, index, bank):
        self.banks.insert(index, bank)

    def delete(self, index):
        del self.banks[index]
        
    @property
    def json(self):
        banks = []
        for bank in self.banks:
            banks.append(bank.data)

        return banks