import re
import datetime


class NicgepParser:

    def __init__(self, name, url, data):
        self.name = name
        self.base = url
        self.data = data

    def string_entry(self, keyname, sqllength=None):
        strvalue = self.data.get(keyname, None)
#       if (strvalue is not None) & (strvalue in ['NA', 'Not Applicable']):
        if (strvalue in [None, 'NA', 'Not Applicable']):
            return None
        else:
            return strvalue[0:sqllength]

    def int_entry(self, keyname):
        intvalue = self.data.get(keyname, None)
        if (intvalue is not None) & (intvalue in ['NA', 'Not Applicable']):
            return None
        else:
            return int(intvalue)

    def bool_entry(self, keyname):
        boolvalue = self.data.get(keyname, None)
        if (boolvalue is not None) & (bool(re.search('^No', boolvalue))):
            return 0
        else:
            return 1

    def float_entry(self, keyname):
        floatvalue = self.data.get(keyname, None)
        if (floatvalue is not None) & (floatvalue not in ['NA', 'Not Applicable']):
            return float(floatvalue.replace(",", "").replace("%", ""))
        else:
            return None

    def date_entry(self, keyname):
        datevalue = self.data.get(keyname, None)
        formatdate = '%d-%b-%Y %I:%M %p'
        if (datevalue is not None) & (datevalue not in ['NA', 'Not Applicable']):
            return datetime.datetime.strptime(datevalue.rstrip(), formatdate)
        else:
            return None

    @staticmethod
    def choosemax(a, b):
        if (a is None) & (b is None):
            return None
        elif (a is not None) & (b is None):
            return a
        elif (a is None) & (b is not None):
            return b
        else:
            return max(a, b)

    def parsed_sql_entry(self):
        entrydict = {
            # Site
            'TenderSiteName': self.name,
            'TenderSiteURL': self.base,
            # Strings
            'OrgChain': self.string_entry('Organisation Chain'),
            'Refno': self.string_entry('Tender Reference Number'),
            'Webid': self.string_entry('Tender ID'),
            'TenderType': self.string_entry('Tender Type'),
            'FormofContract': self.string_entry('Form Of Contract'),
            'TenderCategory': self.string_entry('Tender Category'),
            'PaymentMode': self.string_entry('Payment Mode',10),
            'FeePayTo': self.string_entry('Fee Payable To'),
            'FeePayAt': self.string_entry('Fee Payable At'),
            'EMDFeeType': self.string_entry('EMD Fee Type '),
            'EMDPayTo': self.string_entry('EMD Payable To'),
            'EMDPayAt': self.string_entry('EMD Payable At'),
            'Title': self.string_entry('Title'),
            'WorkDescrip': self.string_entry('Work Description'),
            'PreQual': self.string_entry('NDA/Pre Qualification'),
            'External': self.string_entry('Independent External Monitor/Remarks'),
            'Category': self.string_entry('Product Category'),
            'SubCategory': self.string_entry('Sub category'),
            'ContractType': self.string_entry('Contract Type'),
            'Location': self.string_entry('Location'),
            'PreBidMeetLoc': self.string_entry('Pre Bid Meeting Place'),
            'PreBidMeetAdd': self.string_entry('Pre Bid Meeting Address'),
            'BidOpenLoc': self.string_entry('Bid Opening Place'),
            'Currency': self.string_entry('Currency'),
            'NameofTenderer': self.string_entry('Name'),
            'AddressofTenderer': self.string_entry('Address'),
            # INT
            'Covers': self.int_entry('No. of Covers'),
            'BidValidity': self.int_entry('Bid Validity(Days)'),
            'PeriodofWork': self.int_entry('Period Of Work(Days)'),
            'Pincode': self.int_entry('Pincode'),
            # BOOL
            'TechEval': self.bool_entry('General Technical Evaluation Allowed '),
            'ItemwiseTechEval': self.bool_entry('ItemWise Technical Evaluation Allowed'),
            'BOQMultiCurr': self.bool_entry('Is Multi Currency Allowed For BOQ'),
            'FeeMultiCurr': self.bool_entry('Is Multi Currency Allowed For Fee'),
            'TwoStageBid': self.bool_entry('Allow Two Stage Bidding'),
            'FeeExemp': self.bool_entry('Tender Fee Exemption Allowed'),
            'EMDExemp': self.bool_entry('EMD through BG/ST or EMD Exemption Allowed'),
            'AllowNDATender': self.bool_entry('Should Allow NDA Tender'),
            'AllowPrefBid': self.bool_entry('Allow Preferential Bidder'),
            # FLOAT
            'Tenderamount': self.choosemax(self.float_entry('Tender Fee in ₹  '), self.float_entry('Tender Fee')),
            'EMDamount': self.choosemax(self.float_entry('EMD Amount in ₹ '), self.float_entry('EMD Fee')),
            'EMDPercent': self.float_entry('EMD Percentage'),
            'Value': self.float_entry('Tender Value in ₹ '),
            # DATE
            'PreBidMeetDate': self.date_entry('Pre Bid Meeting Date'),
            'PubDate': self.date_entry('Published Date'),
            'BidOpenDate': self.date_entry('Bid Opening Date'),
            'DownloadStartDate': self.date_entry('Document Download / Sale Start Date'),
            'DownloadEndDate': self.date_entry('Document Download / Sale End Date'),
            'ClariStartDate': self.date_entry('Clarification Start Date'),
            'ClariEndDate': self.date_entry('Clarification End Date'),
            'BidSubStartDate': self.date_entry('Bid Submission Start Date'),
            'BidSubEndDate': self.date_entry('Bid Submission End Date'),
        }
        return entrydict
