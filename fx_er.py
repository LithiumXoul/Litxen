#Thanks to anubhav-narayan on github for this amazing code

from pydub import AudioSegment
from pydub.scipy_effects import low_pass_filter
from pydub.scipy_effects import high_pass_filter
from pydub.scipy_effects import band_pass_filter

def cheap_eq(seg,focus_freq,bandwidth=100,mode="peak",gain_dB=0,order=5):
	'''
	Cheap EQ in PyDub
	Silence=-120dBFS
	I2/I1=2=>3dB SPL Gain
	'''
	if gain_dB>=0:
		if mode=="peak":
			sec=band_pass_filter(seg,focus_freq-bandwidth/2,focus_freq+bandwidth/2,order=order)
			pass
		if mode=="low_shelf":
			sec=low_pass_filter(seg,focus_freq,order=order)
			pass
		if mode=="high_shelf":
			sec=high_pass_filter(seg,focus_freq,order=order)
			pass
		seg=seg.overlay(sec-(3-gain_dB))
		pass
	if gain_dB<0:
		if mode=="peak":
			sec=band_pass_filter(seg,focus_freq-bandwidth/2,focus_freq+bandwidth/2,order=order)
			pass
		if mode=="low_shelf":
			sec=low_pass_filter(seg,focus_freq,order=order)
			pass
		if mode=="high_shelf":
			sec=high_pass_filter(seg,focus_freq,order=order)
			pass
		seg=(seg+gain_dB).overlay(sec-(3+gain_dB))-gain_dB
		pass
	return seg
    