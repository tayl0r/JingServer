__author__ = 'tsteil'

from flask import request, session, escape

class JingServer():
    m_filename = ''
    m_app = None
    m_uploadsDir = "uploads/"

    def __init__(self, app):
        self.m_app = app

    def api(self):

        print self.m_filename
        method = request.args.get('method', None)
        #self.m_app.logger.debug(method)

        # 0 - keep alive
        # method	Screencast.Info.Alive
        # apiKey	800bbfc9-928b-4490-904f-adab687ea4de
        # callSignature	9a653ed6c95b663df36591333f9986cb8c7cca96
        if method == "Screencast.Info.Alive":
            return """<rsp stat="ok">
        <aliveResponse>alive</aliveResponse>
    </rsp>"""

        # 0 - user info
        # method	Screencast.User.GetInfo
        # apiKey	800bbfc9-928b-4490-904f-adab687ea4de
        # callSignature	45d9b025eb31eb3d8842e80ff9b5202dddfa87df
        # emailAddress	tsteil@gmail.com
        if method == "Screencast.User.GetInfo":
            return """<rsp stat="ok">
        <userInfo>
            <userName>TaylorSteil</userName>
            <userId>5e5c31ce-3847-4a76-a034-7050370ae65c</userId>
            <emailAddress>tsteil@gmail.com</emailAddress>
            <featureList>
                <allowCustomTemplates>false</allowCustomTemplates>
            </featureList>
        </userInfo>
    </rsp>"""

        # 1
        # /api/?method=Screencast.Auth.GetCode
        # &apiKey=800bbfc9-928b-4490-904f-adab687ea4de
        # &username=TaylorSteil
        # &hashedPassword=13ed411ddbee10f3ea510335a452cebf8231bc88
        # &callSignature=27c92ec1896f19e78ef7d5524fb463f609764bf1
        if method == "Screencast.Auth.GetCode":
            return """<rsp stat="ok">
        <authCode>3d061381-6b17-499e-8ea0-c119fbe12468</authCode>
    </rsp>"""

        # 1
        # http://www.screencast.com/api/?method=Screencast.Auth.CheckCode
        # &apiKey=800bbfc9-928b-4490-904f-adab687ea4de
        # &callSignature=5edd01de105ab6398996af312c5036a9deeaa4cd
        # &authCode=3d061381-6b17-499e-8ea0-c119fbe12468
        if method == 'Screencast.Auth.CheckCode':
            return """<rsp stat="ok">
        <authCode>3d061381-6b17-499e-8ea0-c119fbe12468</authCode>
        <status>valid</status>
        <userName>TaylorSteil</userName>
    </rsp>"""

        # 2
        # method	Screencast.MediaGroup.FindByUserAndTitle
        # apiKey	800bbfc9-928b-4490-904f-adab687ea4de
        # title	Jing
        # userName	TaylorSteil
        # callSignature	d62dd62e40c7390bf4afe53fbe5777fcf4237c34
        if method == "Screencast.MediaGroup.FindByUserAndTitle":
            return """<rsp stat="ok">
        <mediaGroupId>c91444c6-f478-425b-8cd5-d63cee29a7c6</mediaGroupId>
    </rsp>"""

        # 3
        # method	Screencast.MediaSet.Create
        # apiKey	800bbfc9-928b-4490-904f-adab687ea4de
        # title	2012-03-31_2109
        # callSignature	0b7b32c270b0c4bb70127032cf7860f685f9f6f2
        # authCode	3d061381-6b17-499e-8ea0-c119fbe12468
        if method == "Screencast.MediaSet.Create":
            return """<rsp stat="ok">
        <mediaSetId>47d00206-00e8-4ad3-9452-7b6d7785f0fa</mediaSetId>
    </rsp>"""

        # 4
        # method	Screencast.MediaGroup.AddMediaSet
        # apiKey	800bbfc9-928b-4490-904f-adab687ea4de
        # mediaGroupId	c91444c6-f478-425b-8cd5-d63cee29a7c6
        # callSignature	016a77f714b4ee06afbb948271a984461d9f6d8e
        # authCode	3d061381-6b17-499e-8ea0-c119fbe12468
        # mediaSetId	47d00206-00e8-4ad3-9452-7b6d7785f0fa
        if method == "Screencast.MediaGroup.AddMediaSet":
            return """<rsp stat="ok">
        <status>media set successfully added</status>
    </rsp>"""

        # 5
        # height	808
        # dataLength	61752
        # mediaSetId	47d00206-00e8-4ad3-9452-7b6d7785f0fa
        # callSignature	dbfc657c941a4fc292afed622cef136507ea8bb1
        # fileName	00000008.png
        # method	Screencast.Upload.BeginUpload
        # width	1440
        # authCode	3d061381-6b17-499e-8ea0-c119fbe12468
        # apiKey	800bbfc9-928b-4490-904f-adab687ea4de
        if method == "Screencast.Upload.BeginUpload":
            self.m_filename = request.args.get("fileName")
            # session data does not persist in the Jing client
            #session['filename'] = filename
            self.m_app.logger.debug("set filename to: " + self.m_filename)
            return """<rsp stat="ok">
        <mediaId>b8feb75a-78a1-4031-9774-77bb04242769</mediaId>
        <contentServerUrl>http://content.screencast.com/</contentServerUrl>
    </rsp>"""

        # 6 - the actual file upload
        # offset	0
        # callSignature	ea78e2a5b7a180a5bc1827375ae1464a18651ac4
        # mediaId	b8feb75a-78a1-4031-9774-77bb04242769
        # method	Screencast.Upload.AppendData
        # dataLength	61752
        # authCode	3d061381-6b17-499e-8ea0-c119fbe12468
        # apiKey	800bbfc9-928b-4490-904f-adab687ea4de
        # fileData	fileData
        if request.method == 'POST' and method is None:
            method = request.form['method']
            #self.m_app.logger.debug(method)
            if method == "Screencast.Upload.AppendData":
                #filename = session['filename']
                upload = request.files['fileData']
                f = open(self.m_uploadsDir + self.m_filename, 'a')
                bytes = upload.read()
                f.write(bytes)
                self.m_app.logger.debug("added {} bytes to file {}".format(len(bytes), self.m_filename))
                return """<rsp stat="ok">
        <bytesReceived>61752</bytesReceived>
    </rsp>"""

        # 7
        # authCode	3d061381-6b17-499e-8ea0-c119fbe12468
        # height	808
        # mediaSetId	47d00206-00e8-4ad3-9452-7b6d7785f0fa
        # callSignature	ff439b7d5f3323d56d32bef60f871e0763aeea06
        # mediaId	b8feb75a-78a1-4031-9774-77bb04242769
        # method	Screencast.MediaSet.SetDefaultMedia
        # width	1440
        # duration	0
        # apiKey	800bbfc9-928b-4490-904f-adab687ea4de
        if method == "Screencast.MediaSet.SetDefaultMedia":
            return """<rsp stat="ok">
        <update>success</update>
    </rsp>"""

        # 8 - get the url of the uploaded image
        # method	Screencast.MediaSet.GetUrl
        # apiKey	800bbfc9-928b-4490-904f-adab687ea4de
        # mediaGroupId	c91444c6-f478-425b-8cd5-d63cee29a7c6
        # callSignature	e4e5b2d2285d8d7bb0e9a2088932584846cbdf40
        # authCode	3d061381-6b17-499e-8ea0-c119fbe12468
        # mediaSetId	47d00206-00e8-4ad3-9452-7b6d7785f0fa
        if method == "Screencast.MediaSet.GetUrl":
            return """<rsp stat="ok">
        <url>http://192.168.1.12/uploads/upload.png</url>
    </rsp>"""

        # 9
        # callSignature	bdf09b7dede6b0e32d0950cb4a9668d2f675ab62
        # numberToGet	1
        # mediaGroupId	c91444c6-f478-425b-8cd5-d63cee29a7c6
        # password
        # includeLists	false
        # method	Screencast.MediaGroup.GetInfo
        # authCode	3d061381-6b17-499e-8ea0-c119fbe12468
        # startValue	0
        # apiKey	800bbfc9-928b-4490-904f-adab687ea4de
        if method == "Screencast.MediaGroup.GetInfo":
            return """<rsp stat="ok">
        <mediaGroupId>c91444c6-f478-425b-8cd5-d63cee29a7c6</mediaGroupId>
        <title>Jing</title>
        <description>Place for sharing Jing Files</description>
        <accessLevel>hidden</accessLevel>
        <ownerId>5e5c31ce-3847-4a76-a034-7050370ae65c</ownerId>
        <ownerName>TaylorSteil</ownerName>
        <modifyDate>4/1/2012 4:09:59 AM</modifyDate>
        <password />
        <rssFeed>true</rssFeed>
        <iTunesFeed>true</iTunesFeed>
        <numberOfSets>30</numberOfSets>
        <templateId>2</templateId>
        <size>7157013</size>
        <showMediaOnly>False</showMediaOnly>
        <mediaGroupTotalSize>7157013</mediaGroupTotalSize>
        <mediaSetList>
            <mediaSetId>47d00206-00e8-4ad3-9452-7b6d7785f0fa</mediaSetId>
        </mediaSetList>
        <mediaSetInfoList />
    </rsp>"""

        return """<rsp stat="ok">
        <status>media set's SetIsCommentEnabled flag successfully updated</status>
    </rsp>"""
