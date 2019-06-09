import pandas

sampleFileAllLevels = pandas.read_csv('OnTrackWebsite/sample_levels.csv')
sampleFileOneLevels = pandas.read_csv('OnTrackWebsite/sample_percentiles.csv')

levels = ["I", "II", "III", "IV", "V"]

tests = ["ECAB", "SMWT", "SAROMM", "CEDLpar", "CEDLsc", "EASE", "FSA", "HEALTH", "GMFM"]
for test in tests:
    sampleFileAllLevels.to_csv("OnTrackWebsite/graphData/" + test + "_all_levels.csv")
    for level in levels:
        sampleFileOneLevels.to_csv("OnTrackWebsite/graphData/" + test + "_level" + level + ".csv")