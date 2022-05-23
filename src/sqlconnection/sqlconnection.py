import mysql.connector

class tenderdb:

# [TODO] Change sql password
    def __init__(self):
        self.cnx = mysql.connector.connect(user='sumeetkd', password='test123',
    	host='localhost',
    	database='mydb')


    def insertsql(self, entry):
        cursor = self.cnx.cursor()
        add_tender = ("INSERT INTO TempTenders"
        "(TenderSiteURL, TenderSiteName, OrgChain, Refno, Webid, TenderType, FormofContract, TenderCategory, Covers, TechEval, ItemwiseTechEval, PaymentMode, BOQMultiCurr, FeeMultiCurr, TwoStageBid, Tenderamount, FeePayTo, FeePayAt, FeeExemp, EMDamount, EMDExemp, EMDFeeType, EMDPercent, EMDPayTo, EMDPayAt, Title, WorkDescrip, PreQual, External, Value, Category, SubCategory, ContractType, BidValidity, PeriodofWork, Location, Pincode, PreBidMeetLoc, PreBidMeetAdd, PreBidMeetDate, BidOpenLoc, AllowNDATender, AllowPrefBid, PubDate, BidOpenDate, DownloadStartDate, DownloadEndDate, ClariStartDate, ClariEndDate, BidSubStartDate, BidSubEndDate, NameofTenderer, AddressofTenderer, Currency)"
               "VALUES (%(TenderSiteURL)s, %(TenderSiteName)s, %(OrgChain)s, %(Refno)s, %(Webid)s, %(TenderType)s, %(FormofContract)s, %(TenderCategory)s, %(Covers)s, %(TechEval)s, %(ItemwiseTechEval)s, %(PaymentMode)s, %(BOQMultiCurr)s, %(FeeMultiCurr)s, %(TwoStageBid)s, %(Tenderamount)s, %(FeePayTo)s, %(FeePayAt)s, %(FeeExemp)s, %(EMDamount)s, %(EMDExemp)s, %(EMDFeeType)s, %(EMDPercent)s, %(EMDPayTo)s, %(EMDPayAt)s, %(Title)s, %(WorkDescrip)s, %(PreQual)s, %(External)s, %(Value)s, %(Category)s, %(SubCategory)s, %(ContractType)s, %(BidValidity)s, %(PeriodofWork)s, %(Location)s, %(Pincode)s, %(PreBidMeetLoc)s, %(PreBidMeetAdd)s, %(PreBidMeetDate)s, %(BidOpenLoc)s, %(AllowNDATender)s, %(AllowPrefBid)s, %(PubDate)s, %(BidOpenDate)s, %(DownloadStartDate)s, %(DownloadEndDate)s, %(ClariStartDate)s, %(ClariEndDate)s, %(BidSubStartDate)s, %(BidSubEndDate)s, %(NameofTenderer)s, %(AddressofTenderer)s, %(Currency)s)")
        cursor.execute(add_tender,entry)
        cursor.close()
        self.cnx.commit()

    def updatedb(self):
        cursor = self.cnx.cursor()
        combine = ("INSERT INTO Tenders "
                   "SELECT * FROM TempTenders AS temp "
                   "ON DUPLICATE KEY UPDATE "
                   "OrgChain=                temp.OrgChain,"
                   "Refno=			 temp.Refno,"
                   "TenderType=		 temp.TenderType,"
                   "FormofContract=		 temp.FormofContract,"
                   "TenderCategory=		 temp.TenderCategory,"
                   "Covers=			 temp.Covers,"
                   "TechEval=		 temp.TechEval,"
                   "ItemwiseTechEval=	 temp.ItemwiseTechEval,"
                   "PaymentMode=		 temp.PaymentMode,"
                   "BOQMultiCurr=		 temp.BOQMultiCurr,"
                   "FeeMultiCurr=		 temp.FeeMultiCurr,"
                   "TwoStageBid=		 temp.TwoStageBid,"
                   "Tenderamount=		 temp.Tenderamount,"
                   "FeePayTo=		 temp.FeePayTo,"
                   "FeePayAt=		 temp.FeePayAt,"
                   "FeeExemp=		 temp.FeeExemp,"
                   "EMDamount=		 temp.EMDamount,"
                   "EMDExemp=		 temp.EMDExemp,"
                   "EMDFeeType=		 temp.EMDFeeType,"
                   "EMDPercent=		 temp.EMDPercent,"
                   "EMDPayTo=		 temp.EMDPayTo,"
                   "EMDPayAt=		 temp.EMDPayAt,"
                   "Title=			 temp.Title,"
                   "WorkDescrip=		 temp.WorkDescrip,"
                   "PreQual=		 temp.PreQual,"
                   "External=		 temp.External,"
                   "Value=			 temp.Value,"
                   "Category=		 temp.Category,"
                   "SubCategory=		 temp.SubCategory,"
                   "ContractType=		 temp.ContractType,"
                   "BidValidity=		 temp.BidValidity,"
                   "PeriodofWork=		 temp.PeriodofWork,"
                   "Location=		 temp.Location,"
                   "Pincode=		 temp.Pincode,"
                   "PreBidMeetLoc=		 temp.PreBidMeetLoc,"
                   "PreBidMeetAdd=		 temp.PreBidMeetAdd,"
                   "PreBidMeetDate=		 temp.PreBidMeetDate,"
                   "BidOpenLoc=		 temp.BidOpenLoc,"
                   "AllowNDATender=		 temp.AllowNDATender,"
                   "AllowPrefBid=		 temp.AllowPrefBid,"
                   "PubDate=		 temp.PubDate,"
                   "BidOpenDate=		 temp.BidOpenDate,"
                   "DownloadStartDate=	 temp.DownloadStartDate,"
                   "DownloadEndDate=	 temp.DownloadEndDate,"
                   "ClariStartDate=		 temp.ClariStartDate,"
                   "ClariEndDate=		 temp.ClariEndDate,"
                   "BidSubStartDate=	 temp.BidSubStartDate,"
                   "BidSubEndDate=		 temp.BidSubEndDate,"
                   "NameofTenderer=		 temp.NameofTenderer,"
                   "AddressofTenderer=	 temp.AddressofTenderer,"
                   "Currency=		 temp.Currency")
        clean_temp = "TRUNCATE TABLE TempTenders"
        cursor.execute(combine)
        cursor.execute(clean_temp)
        cursor.close()
        self.cnx.commit()
        self.cnx.close()
