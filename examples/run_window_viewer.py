import SpectrumViewer.mvcViewer as mvc

fileName = './example_lite.fits'
#fileName = './example_pfsObject.fits'
fileSource = 'SDSS'
#mvc.window_view(fileName,fileSource, residual = True, other =True)
mvc.window_view(fileName,fileSource)