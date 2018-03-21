import SpectrumViewer.specController as C
import SpectrumViewer.specModel as M
import SpectrumViewer.specView as V
import SpectrumViewer.SDSSDriver as driver
def view(filename,filesource):
    coaddObj, zObj = driver.loadFITS(filename, filesource)
    m = M.SpecModel(coaddObj, zObj)
    v = V.SpecView(filename)
    c = C.SpecController(m,v)
    c.run()
    #c.controlFunc('Other')

# fileName = 'example_lite.fits'
# fileSource = 'SDSS'
#
# view(fileName,fileSource)