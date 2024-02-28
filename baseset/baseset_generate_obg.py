import sys
import os
import glob

blitter = 8
typelong = "8-bit"
typeshort = "8"

if len(sys.argv) > 1:
  # settings
  if "32" in sys.argv[1]:
    blitter = 32
    typelong = "32-bit"
    typeshort = "32"
  if "ez" in sys.argv[1]:
    typeshort += "ez"
    typelong += " Extra Zoom"
  else:
    typelong += " Normal Zoom"

defaultlngid = "0x01"
lngids = {
  "0x00": "en_US",
  "0x01": "en_GB",
  "0x02": "de_DE",
  "0x03": "fr_FR",
  "0x04": "es_ES",
  "0x05": "eo_EO",
  "0x06": "io_IO",
  "0x07": "ru_RU",
  "0x08": "ga_IE",
  "0x09": "mt_MT",
  "0x0a": "ta_IN",
  "0x0b": "cv_RU",
  "0x0c": "zh_TW",
  "0x0d": "sr_RS",
  "0x0e": "nn_NO",
  "0x0f": "cy_GB",
  "0x10": "be_BY",
  "0x11": "mr_IN",
  "0x12": "fo_FO",
  "0x13": "gd_GB",
  "0x14": "ar_EG",
  "0x15": "cs_CZ",
  "0x16": "sk_SK",
  "0x17": "hi_IN",
  "0x18": "bg_BG",
  #0x19
  #0x1a
  "0x1b": "af_ZA",
  #0x1c
  #0x1d
  "0x1e": "el_GR",
  "0x1f": "nl_NL",
  #0x20
  "0x21": "eu_ES",
  "0x22": "ca_ES",
  "0x23": "lb_LU",
  "0x24": "hu_HU",
  #0x25
  "0x26": "mk_MK",
  "0x27": "it_IT",
  "0x28": "ro_RO",
  "0x29": "is_IS",
  "0x2a": "lv_LV",
  "0x2b": "lt_LT",
  "0x2c": "sl_SI",
  "0x2d": "da_DK",
  "0x2e": "sv_SE",
  "0x2f": "nb_NO",
  "0x30": "pl_PL",
  "0x31": "gl_ES",
  "0x32": "fy_NL",
  "0x33": "uk_UA",
  "0x34": "et_EE",
  "0x35": "fi_FI",
  "0x36": "pt_PT",
  "0x37": "pt_BR",
  "0x38": "hr_HR",
  "0x39": "ja_JP",
  "0x3a": "ko_KR",
  #0x3b
  "0x3c": "ms_MY",
  "0x3d": "en_AU",
  "0x3e": "tr_TR",
  #0x3f
  #0x40
  #0x41
  "0x42": "th_TH",
  #0x43
  # |
  #0x53
  "0x54": "vi_VN",
  "0x55": "es_MX",
  "0x56": "zh_CN",
  #0x57
  #0x58
  #0x59
  "0x5a": "id_ID",
  #0x5b
  "0x5c": "ur_PK",
  #0x5d
  # |
  #0x60
  "0x61": "he_IL",
  "0x62": "fa_IR",
  #0x63
  #0x64
  #0x65
  "0x66": "la_VA",
}

# load translateable strings
lngfiles = glob.glob(os.path.join("lang", "*.lng"))
lngs = {}
for lngfile in lngfiles:
  with open(lngfile, "r") as f:
    lines = f.read().splitlines()
    langid = lines[0][len("##grflangid "):]
    lngs[langid] = {x.split(":")[0].strip(): x.split(":")[1].strip() if ":" in x else None for x in lines[1:]}

# catch specific variant cases, release cases (8, 32ez)
if typeshort == "8":
  descriptionstrid = "STR_OBG_DESCRIPTION_VARIANT_CLASSIC"
  namesuffix = "Classic"
elif typeshort == "32ez":
  descriptionstrid = "STR_OBG_DESCRIPTION_VARIANT_HIGHDEF"
  namesuffix = "High Def"
else:
  description = typelong
  namesuffix = typelong

# define unique short (4 character) names
namelookup = {"8": "ogfx", "8ez": "ogfX", "32": "ogFx", "32ez": "ogFX"}


def pad(string, length, character=" ", pad_left=True):
  out = string
  if pad_left:
    return character * (length - len(string)) + out
  else:
    return out + character * (length - len(string))

files = [
  {"type": "base", "name": "ogfx21_base_" + typeshort},
  {"type": "arctic", "name": "ogfx2c_arctic_" + typeshort},
  {"type": "tropical", "name": "ogfx2h_tropical_" + typeshort},
  {"type": "toyland", "name": "ogfx2t_toyland_" + typeshort},
  {"type": "logos", "name": "ogfx2i_logos_" + typeshort}, 
  {"type": "extra", "name": "ogfx2e_extra_" + typeshort}
]

with open("opengfx2_" + typeshort + ".obg", "w") as obg:
  obg.write("[metadata]" + "\n")
  pad_length = 12
  obg.write(pad("name", pad_length, pad_left=False) + "= OpenGFX2 " + namesuffix + "\n")
  obg.write(pad("shortname", pad_length, pad_left=False) + "= " + namelookup[typeshort] + "\n")
  obg.write(pad("version", pad_length, pad_left=False) + "= 5" + "\n")
  obg.write(pad("palette", pad_length, pad_left=False) + "= DOS" + "\n")
  obg.write(pad("blitter", pad_length, pad_left=False) + "= "+str(blitter)+"bpp" + "\n")
  # write all non-default languages with translations available
  for lng in lngs:
    if lng != defaultlngid:
      descriptionmain = lngs[lng]["STR_OBG_DESCRIPTION_MAIN"] if "STR_OBG_DESCRIPTION_MAIN" in lngs[lng] else lngs[defaultlngid]["STR_OBG_DESCRIPTION_MAIN"]
      descriptionvariant = lngs[lng][descriptionstrid] if descriptionstrid in lngs[lng] else lngs[defaultlngid][descriptionstrid]
      descriptionextra = lngs[lng]["STR_OBG_DESCRIPTION_EXTRA"] if "STR_OBG_DESCRIPTION_EXTRA" in lngs[lng] else lngs[defaultlngid]["STR_OBG_DESCRIPTION_EXTRA"]
      descriptionversion = lngs[defaultlngid]["STR_OBG_DESCRIPTION_VERSION"]
      if lng == "0x56" or lng == "0x0c":
        # Some languages' punctuations are different. They don't have spaces after commas and periods. In this case it's zh_CN and zh_TW.
        obg.write(pad("description." + lngids[lng], pad_length, pad_left=False) + "= " + descriptionmain + descriptionvariant + descriptionextra + "(" + typelong + ")" + descriptionversion + "\n")
      else:
        obg.write(pad("description." + lngids[lng], pad_length, pad_left=False) + "= " + descriptionmain + " " + descriptionvariant + " " + descriptionextra + "(" + typelong + ")" + descriptionversion + "\n")
  # write default language as special case
  obg.write(pad("description", pad_length, pad_left=False) + "= " + lngs[defaultlngid]["STR_OBG_DESCRIPTION_MAIN"] + " " + lngs[defaultlngid][descriptionstrid] + " " + lngs[defaultlngid]["STR_OBG_DESCRIPTION_EXTRA"] + "(" + typelong + ")" + lngs[defaultlngid]["STR_OBG_DESCRIPTION_VERSION"] + "\n")
  obg.write("\n")
  obg.write("[files]" + "\n")
  for file in files:
    obg.write(pad(file["type"], 12, pad_left=False) + "= " + file["name"] + ".grf" + "\n")
  obg.write("\n")
  obg.write("[md5s]" + "\n")
  for file in files:
    if "md5" in file:
      md5 = file["md5"] + "\n"
    else:
      with open(file["name"] + ".md5", "r") as md5_file:
        md5 = md5_file.read()
    obg.write(pad(file["name"] + ".grf", 26, pad_left=False) + "= " + md5)
  obg.write("\n")
  obg.write("[origin]" + "\n")
  obg.write("default = From the in-game content download system (BaNaNaS) or https://github.com/zephyris/opengfx2/")
