from scipy.stats import norm

import matplotlib.mlab as mlab

import matplotlib.pyplot as plt

from numpy import histogram

from patents import documents

ligs = []
n = 0



for p in documents:
    print documents[p]
    try:
        ligs.append(int(documents[p][4]))
    except:
        ligs.append(0)
    n += 1

(mu, sigma) = norm.fit(ligs)
n, bins, patches = plt.hist(ligs, 60, normed=1, facecolor='green', alpha=0.75)

y = mlab.normpdf(bins, mu, sigma)

plt.plot(bins, y, 'r--', linewidth=2)
plt.ylabel("Amount of Patents")
plt.xlabel("Litigation Cases Total")
plt.show()
