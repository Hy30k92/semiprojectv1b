from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from app.dbfactory import get_db
from app.schema.member import NewMember
from app.service.member import MemberService

member_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')


@member_router.get('/join', response_class=HTMLResponse)
async def join(req: Request):
    return templates.TemplateResponse('member/join.html', {'request': req})

@member_router.post('/join', response_class=HTMLResponse)

async def joinok(member: NewMember, db: Session = Depends(get_db)):
    try:
        if MemberService.check_captcha(member):

            print(member)
            result = MemberService.insert_member(db,member)
            print('처리결과 : ', result.rowcount)

            if result.rowcount > 0: # 회원가입이 성공적으로 완료되면 페이지 이동
                return RedirectResponse(url='/member/login', status_code=303)
        else:
            return RedirectResponse(url='/member/login', status_code=303)


    except Exception as ex:
        print(f' ▷▷▷ joinok 오류발생 : {str(ex)}')
        return RedirectResponse(url='/member/error', status_code=303)

@member_router.get('/login', response_class=HTMLResponse)
async def loginok(req: Request ):
    return templates.TemplateResponse('member/login.html', {'request': req})

@member_router.post('/login', response_class=HTMLResponse)
async def login(req: Request, db: Session = Depends(get_db)):
    data = await req.json() # 클라이언트가 보낸 데이터를 request 객체로 받음
    try:
        print('전송한 데이터 : ', data)
        redirect_url = '/member/loginfail' # 로그인 실패시

        if MemberService.login_member(db. data): # 로그인 성공시
            redirect_url = '/member/myinfo' # myinfo로 이동

        return RedirectResponse(url=redirect_url, status_code=303)

    except Exception as ex:
        print(f'login 오류 : {str(ex)}')
        return RedirectResponse(url='/member/error', status_code=303)


@member_router.get('/myinfo', response_class=HTMLResponse)
async def myinfo(req: Request):
    return templates.TemplateResponse('member/myinfo.html', {'request': req})

@member_router.get('/error', response_class=HTMLResponse)
async def error(req: Request):
    return templates.TemplateResponse('member/error.html', {'request': req})



