from dataclasses import dataclass, field
from datetime import date
from typing import List


##########################################################
# Crop
##########################################################

@dataclass
class Crop:

    crop_name: str

    sowing_date: date

    premium_debit_date: date

    survey_numbers: List[str] = field(default_factory=list)


##########################################################
# Khata
##########################################################

@dataclass
class Khata:

    khata_no: str

    khasra_no: str

    crops: List[Crop] = field(default_factory=list)

    #######################################################

    def add_crop(self, crop: Crop):

        self.crops.append(crop)
    
    def find_crop(self, crop_name: str):

        for crop in self.crops:

            if crop.crop_name == crop_name:
                return crop

        return None


##########################################################
# Account
##########################################################

@dataclass
class Account:

    account_no: str

    district: str

    mandal: str

    gram_panchayat: str

    village: str

    khatas: List[Khata] = field(default_factory=list)

    #######################################################

    def add_khata(self, khata: Khata):

        self.khatas.append(khata)

    def find_khata(self, khata_no: str):

        for khata in self.khatas:

            if khata.khata_no == khata_no:
                return khata

        return None
    
    

