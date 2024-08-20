# SemiProject v1b


## 프로젝트에 사용한 모듈들
+ FastAPI, uvicorn
+ Jinja2
+ sqlalchemy


## 프로젝트 기본 구조
+ 설정(디비) : dbfactory , settings
+ model (디비-테이블): Member
+ schema (유효성 검사): NewMember
+ service (CRUD) : MemberService
+ route (url - 진입점(엔드포인트) 제공): member_router
