#!/usr/bin/python3

from scipy import stats

import matplotlib.pyplot as pyplot

# generate a sample of uniformly distributed data
x = stats.uniform.rvs(size=500)
#print(x)

# Probability plot for the theoretical uniform vs uniform samples
f1, ax1 = pyplot.subplots()
res = stats.probplot(x, dist=stats.uniform, plot=pyplot)
ax1.set_title("Probplot for uniform vs uniform samples")
ax1.grid(b=True, which='major', color='#CCCCCC', linestyle='-')
pyplot.show()


# Probability plot for the theoretical exponential vs uniform samples
f1, ax1 = pyplot.subplots()
res = stats.probplot(x, dist=stats.expon, plot=pyplot)
ax1.set_title("Probplot for exponential vs uniform samples")
ax1.grid(b=True, which='major', color='#CCCCCC', linestyle='-')
pyplot.show()


# generate a sample of exponentially distributed data
x = stats.expon.rvs(loc=1, scale=3, size=500)

# theoretical exponential vs exponential samples
f1, ax1 = pyplot.subplots()
res = stats.probplot(x, dist=stats.expon, plot=pyplot)
ax1.set_title("Probplot for exponential vs exponential samples")
ax1.grid(b=True, which='major', color='#CCCCCC', linestyle='-')
pyplot.show()

# theoretical exponential vs exponential samples with different parameters
f1, ax1 = pyplot.subplots()
res = stats.probplot(x, dist=stats.expon, sparams=(1, 2), plot=pyplot)
ax1.set_title("Probplot for scaled exponential vs exponential samples")
ax1.grid(b=True, which='major', color='#CCCCCC', linestyle='-')
ax1.plot([0, 20], [0, 20])
pyplot.show()

# fit an exponential distribution to the data
print(stats.expon.fit(x))
