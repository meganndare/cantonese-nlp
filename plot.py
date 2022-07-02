import pickle
import matplotlib.pyplot as plt

with open('can_stat.pkl', 'rb') as f:
    len_dict = pickle.load(f)

sent_len = sorted(len_dict.keys())
print(sent_len)
amount = [len_dict[i] for i in sent_len]

plt.bar(sent_len, amount)
plt.xlim(0, 50)
plt.xlabel("sentence length (punctuation included)")
plt.ylabel("frequency")

plt.show()
