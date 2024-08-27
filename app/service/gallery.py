import os
from datetime import datetime

from fastapi import Form
from sqlalchemy import insert, select, distinct, func
from sqlalchemy.orm import aliased

from app.model.gallery import GalAttach, Gallery
from app.schema.gallery import NewGallery

UPLOAD_PATH = 'C:/java/nginx-1.26.2/html/cdn/img/'

def get_gallery_data(title: str = Form(...), userid: str = Form(...),
                     contents: str = Form(...), captcha: str = Form(...)):
    return NewGallery(userid=userid, title=title,
                      contents=contents, captcha=captcha)


async def process_upload(files):
    attachs = [] # 업로드 된 파일정보를 저장하기 위해 리스트 생성
    today = datetime.today().strftime('%Y%m%d%H%M%S') # UUID 생성
    for file in files:
        if file.filename != '' and file.size > 0:
            nfname = f'{today}{file.filename}'
            # os.path.join(A,B) => A/B(경로생성)
            fname = os.path.join(UPLOAD_PATH, nfname) # 업로드할 파일경로 생성
            content = await file.read()     # 업로드할 파일의 내용을 비동기로 읽음
            with open(fname, 'wb') as f:
                f.write(content)
            attach = [nfname, file.size]
            attachs.append(attach)

    return attachs

class GalleryService:
    @staticmethod
    def insert_gallery(gal, attachs, db):
        try:
            stmt = insert(Gallery).values(userid=gal.userid,
                            title=gal.title, contents=gal.contents)
            result = db.execute(stmt)

            # 방금 생성ㅎ안 레코드의 기본 키 값 : inserted_primary_key
            inserted_gno = result.inserted_primary_key[0]
            for attach in attachs:
                data = {'fname': attach[0], 'fsize': attach[1],
                        'gno': inserted_gno }
                stmt = insert(GalAttach).values(data)
                result = db.execute(stmt)

            db.commit()

            return result

        except Exception as ex:
            print(f' ▶▶▶ insert_gallery 에서 오류 발생: {str(ex)} ')
            db.rollback()

    @staticmethod
    def select_gallery(cpg, db):
        try:
            stmt = select(distinct(Gallery.gno).label('gno'),
                  Gallery.title, Gallery.userid,
                  Gallery.regdate, Gallery.views,
                  func.first_value(GalAttach.fname) \
                  .over(partition_by=Gallery.gno).label('fname')) \
            .join_from(Gallery, GalAttach) \
            .order_by(Gallery.gno.desc()).limit(25)
            result = db.execute(stmt).fetchall()
            return result

        except Exception as ex:
            print(f' ▶▶▶ select_gallery 에서 오류 발생: {str(ex)} ')
            db.rollback()

    @staticmethod
    def selectone_gallery(gno, db):
        try:

           stmt = select(Gallery, GalAttach)\
               .join_from(Gallery, GalAttach)\
               .where(Gallery.gno == gno)
           result = db.execute(stmt).fetchall()

           return result

        except Exception as ex:
            print(f' ▶▶▶ selectone_gallery 에서 오류 발생: {str(ex)} ')
            db.rollback()