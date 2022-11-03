# --------------------------------------
#
# Process errors in CLOCK
#
# --------------------------------------
def clockError(clock, file=""):
  if clock["errorInCLOCK"] == "unparseableCLOCK":
    print("Error in parsing file %s, %s" % (file, clock["CLOCK"]))

  if clock["errorInCLOCK"] == "differentDays":
    print("ERROR! Clocking in different days in file %s: %s <> %s" % \
      (file, clock["startDate"], clock["endDate"]))

  if clock["errorInCLOCK"] == "startBiggerThanEnd":
    print("ERROR! Start time bigger than end time in file %s: %s > %s" % \
      (file, clock["startHour"], clock["endHour"]))

  if clock["errorInCLOCK"] == "unparseableTimestamp":
    print("ERROR! Unparseable timestamp in file %s: %s" % \
      (file, clock["timestamp"]))
