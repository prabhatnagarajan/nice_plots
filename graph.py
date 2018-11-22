from pdb import set_trace
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rc
# rc('text', usetex=True)
from scipy.interpolate import interp1d

#try bmh
plt.style.use('bmh')
from pdb import set_trace

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
			xs = [range(len(ys[i])) for i in range(len(ys))]
		self.label = label
		self.xs = xs
		self.ys = ys
		self.plot_ci = plot_ci

	def x_axis(self):
		num_points = min([len(points) for points in self.ys])
		min_x = max([min(xs) for xs in self.xs])
		max_x = min([max(xs) for xs in self.xs])
		increment = (max_x - min_x)/num_points
		x_vals = [point * increment + min_x for point in range(num_points)]
		if max_x not in x_vals:
			x_vals.append(max_x)
		return x_vals


	def mean(self):
		sample_size = len(self.ys)
		interp_ys = [interp1d(self.xs[i], self.ys[i]) for i in range(len(self.ys))]
		x_vals = self.x_axis()
		mean = [float(sum([f(i) for f in interp_ys]))/float(sample_size) for i in x_vals]
		return mean

	def ci_error(self):
		if len(self.ys) <= 1:
			return [0 for _ in range(len(self.x_axis()))]
		interp_ys = [interp1d(self.xs[i], self.ys[i]) for i in range(len(self.ys))]
		error = [ci([f(i) for f in interp_ys]) for i in self.x_axis()]
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
			p = plt.plot(np.array(curve.x_axis()), mean, label=curve.label)
			error = np.array(curve.ci_error())
			if curve.plot_ci:
				plt.fill_between(np.array(curve.x_axis()), mean - error, mean + error,
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