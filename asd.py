from txtdata import TxtData

txt = TxtData()
txt.insert({'A': 123})
txt.insert(B=111)
print(txt.data)
print(txt.to_txt())
