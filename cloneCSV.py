import pandas

sampleFileAllLevels = pandas.read_csv('OnTrackWebsite/sample_levels.csv')
sampleFileOneLevels = pandas.read_csv('OnTrackWebsite/sample_percentiles.csv')

tests = ["ECAB", "SMWT", "SAROMM", "CEDLpar", "CEDLsc", "EASE", "FSA", "HEALTH", "GMFM"]
for test in tests:
    sampleFileAllLevels.to_csv("OnTrackWebsite/graphData/" + test + "_all_levels.csv")
    for level in range(1,5):
        sampleFileOneLevels.to_csv("OnTrackWebsite/graphData/" + test + "_level" + str(level) + ".csv")