import importlib
import openalexraw

from pathlib import Path

importlib.reload(openalexraw)

openAlexPath = Path('../../../santo_project/openalex-snapshot')

oa = openalexraw.OpenAlex(
    openAlexPath = openAlexPath
    #Path to OpenAlex data
)


outputLocation = ""
#Path to the output

# entityType = "concepts"
# openalexraw.archive.createTSV(oa,entityType, outputLocation, selection=["core","basic"])

# entityType = "funders"
# openalexraw.archive.createTSV(oa,entityType, outputLocation, selection=["core","basic"])

entityType = "institutions"
openalexraw.archive.createTSV(oa,entityType, outputLocation, selection=["core","basic","ids"])

# entityType = "publishers"
# openalexraw.archive.createTSV(oa,entityType, outputLocation, selection=["core","basic"])

# entityType = "sources"
# openalexraw.archive.createTSV(oa,entityType, outputLocation, selection=["core","basic","ids"])

entityType = "authors"
openalexraw.archive.createTSV(oa,entityType, outputLocation, selection=["core","basic","ids"])

entityType = "works"
openalexraw.archive.createTSV(oa,entityType, outputLocation,
                               selection=["core","basic","authorship","ids",
                                          "funding","concepts","references","mesh"])