import csv
import json

def convert_pkg_cat_csv_json():
  pkg_catagory = csv.DictReader(open("ProductDefinition.csv",'r'))
  pkgCatDict = dict() # create a package info direct from csv file
  catPkgDict = dict() # store the Cat, Dict
  curCat = None
  curCap = None
  for fields in pkg_catagory:
    pkgCat = fields['Category']
    if pkgCat:
      curCat = pkgCat
      if curCat not in catPkgDict:
        catPkgDict[curCat] = dict()
      continue
    pkgCap = fields['Capacity']
    if pkgCap:
      curCap = pkgCap
      if curCap not in catPkgDict[curCat]:
        catPkgDict[curCat][curCap] = set()
      continue
    pkgName = fields['Package Name']
    if pkgName:
      if curCat and curCap:
        catPkgDict[curCat][curCap].add(pkgName)
      else:
        print "error"
      pkg = fields['DSS Package']
      pkgCatDict[pkgName] = [fields['DSS Package'], fields['VA Package'],
          fields['OSEHRA Package']]

  packageJson = generate_output_json_dict(catPkgDict, pkgCatDict)
  output = json.dumps(packageJson)
  outputFile = open("packages.json", 'w')
  outputFile.write(output)
  outputFile.write("\n")

def generate_output_json_dict(inputDict, pkgCatDict):
 # read package.csv file for more information
  packages_csv = csv.DictReader(open("Packages.csv",'r'))
  pkgNameSet = set()
  pkgNamePrex = dict()
  pkg = None
  for fields in packages_csv:
    if fields['Directory Name']:
      pkg = fields['Directory Name']
      pkgNameSet.add(pkg)
      pkgNamePrex[pkg] = []
    if pkg and fields['Prefixes']:
      pkgNamePrex[pkg].append(fields['Prefixes'])

  packageJson = dict() # the final json structure and convert to json file
  packageJson["name"] = "VistA"
  packageJson["children"] = []

  for key, value in inputDict.iteritems():
    outItem = dict()
    outItem['name'] = key
    if value and len(value) > 0:
      outItem['children'] = []
      for key2, val2 in value.iteritems():
        outCapItem = dict()
        outCapItem['name'] = key2
        if val2 and len(val2) > 0:
          outCapItem['children'] = []
          for pkg in val2:
            outPkg = dict()
            outPkg['name'] = pkg
            if pkg in pkgNameSet:
              outPkg['hasLink'] = True
              outPkg['prefixes'] = pkgNamePrex[pkg]
            else:
              outPkg['hasLink'] = False
            if pkg in pkgCatDict:
              infoLst = pkgCatDict[pkg]
              outPkg['category'] = []
              if pkg in pkgNameSet:
                outPkg['category'].extend(['VA Packages', 'OSEHRA Packages'])
              else:
                outPkg['category'].extend(['DSS Packages'])
              """ comment out this part until we have a distribution list
              if infoLst[0] == '1':
                outPkg['category'].append('DSS Package')
              if infoLst[1] == '1':
                outPkg['category'].append('VA Package')
              if infoLst[2] == '1':
                outPkg['category'].append('OSEHRA Package')
              """
            outCapItem['children'].append(outPkg)
        outItem['children'].append(outCapItem)
    packageJson['children'].append(outItem)

  return packageJson

def main():
  convert_pkg_cat_csv_json()

if __name__ == '__main__':
  main()

