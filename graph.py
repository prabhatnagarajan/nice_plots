from pdb import set_trace
import collections
import numpy as np
import matplotlib.colors as mc
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rc
# rc('text', usetex=True)

#try bmh
plt.style.use('bmh')


def sample_sd(data):
	return np.std(data, ddof=1)

'''
95% CI
'''
def ci(data):
	return sample_sd(data) * 1.96

def relative_sd(data):
	return 100.0 * sample_sd(data)/abs(np.mean(data))

class Curve:
	'''
	List of lists of curves
	'''
	def __init__(self, ys, xs=None, label=None, plot_ci=True):
		if not xs:
			xs = range(len(ys[0]))
		self.label = label
		self.xs = xs
		self.ys = ys
		self.plot_ci = plot_ci

	def mean(self):
		sample_size = len(self.ys)
		mean = [float(sum([y[i] for y in self.ys]))/float(sample_size) for i in range(len(self.ys[0]))]
		return mean
	
	def ci_error(self):
		if len(self.ys) <= 1:
			return [0 for _ in range(len(self.ys[0]))]
		error = [ci([y[i] for y in self.ys]) for i in range(len(self.ys[0]))]
		return error

class Plot:
	def __init__(self, curves=[], file=None,
		title=None, xlabel=None, ylabel=None,
		legend=True):
		self.curves = curves
		self.filename = file
		self.title=title
		self.xlabel = xlabel
		self.ylabel = ylabel
		self.legend = legend

	def add_curve(self, curve):
		self.curves.append(curve)

	def set_file(file):
		self.filename = file

	def plot(self):
		plt.clf()
		axes = plt.gca()
		for curve in self.curves:
			mean = np.array(curve.mean())
			p = plt.plot(np.array(curve.xs), mean, label=curve.label)
			error = np.array(curve.ci_error())
			if curve.plot_ci:
				plt.fill_between(np.array(curve.xs), mean - error, mean + error,
				 alpha=0.5, edgecolor=p[0].get_color(),
				facecolor=p[0].get_color())
		# axes.set_ylim([0.0, 4.1])
		if self.legend:
			plt.legend(loc='best')
		if self.title:
			plt.title(self.title)
		if self.xlabel:
			plt.xlabel(self.xlabel)
		if self.ylabel:
			plt.ylabel(self.ylabel)
		if self.filename:
			plt.savefig(self.filename)