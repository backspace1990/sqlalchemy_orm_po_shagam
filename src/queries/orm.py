from sqlalchemy import select, func, cast, Integer, and_, insert
from database import sync_engine, session_faktory, Base, asyn_session_faktory
from models import  WorkersOrm, ResumesOrm, Workload
from sqlalchemy.orm import aliased


class SyncORM:
    @staticmethod
    def create_tables():
        sync_engine.echo = True
        Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine)
        sync_engine.echo = True

    @staticmethod
    def insert_data():
        with session_faktory() as session:
            workers_bobr = WorkersOrm(username="Bobr")
            workers_volk = WorkersOrm(username="Volk")
            session.add_all([workers_bobr, workers_volk])
            session.commit()
    
    @staticmethod
    def select_workers():
        with session_faktory() as session:
            #worker_id = 1
            #worker_Jack = session.get(WorkersOrm, worker_id)
            query = select(WorkersOrm) 
            result = session.execute(query)
            workers = result.scalars().all()
            print(f"{workers=}")


    @staticmethod
    def update_workers(worker_id: int = 1, new_username: str = "LEVENT"):
        with session_faktory() as session:
            worker_jack = session.get(WorkersOrm, worker_id)
            worker_jack.username = new_username
            session.commit()
    
    @staticmethod
    def insert_resumes():
        with session_faktory() as session:
            resume_bobr_1 = ResumesOrm(title="Python Junior Developer", compensation=50000, workload=Workload.fulltime, worker_id=1)
            resume_bobr_2 = ResumesOrm(title="Python Разработчик", compensation=150000, workload=Workload.fulltime, worker_id=1)
            resume_volk_1 = ResumesOrm(title="Python Data Engineer", compensation=250000, workload=Workload.parttime, worker_id=2)
            resume_volk_2 = ResumesOrm(title="Data Scientist", compensation=300000, workload=Workload.fulltime, worker_id=2)
            session.add_all([resume_bobr_1, resume_bobr_2, resume_volk_1, resume_volk_2])
            session.commit()
            sync_engine.echo = True
    
    @staticmethod
    def select_resumes_avg_compensation(like_language: str = "Python"):
        """
            select workload, avg(compensation)::int as avg_compensation
            from resumes
            where title like '%Python%' and compensation > 40000
            group by workload
        """
        with session_faktory() as session:
            query = (
                select(
                    ResumesOrm.workload,
                    cast(func.avg(ResumesOrm.compensation), Integer).label("avg_compensation"),
                )
                .select_from(ResumesOrm)
                .filter(and_(
                    ResumesOrm.title.contains(like_language),
                    ResumesOrm.compensation > 40000,
                ))
                .group_by(ResumesOrm.workload)
                .having(cast(func.avg(ResumesOrm.compensation), Integer) > 70000)
            )
            print(query.compile(compile_kwargs={"literal_binds": True}))
            res = session.execute(query)
            result = res.all()
            print(result)
            print(result[0].avg_compensation)
            print(result[1].avg_compensation)
    
    @staticmethod
    async def insert_additional_resumes():
        async with asyn_session_faktory() as session:
            workers = [
                {"username": "Artem"},
                {"username": "Roman"},
                {"username": "Petr"},
            ]
            resumes = [
                {"title":"Python Программист", "compensation": 60000, "workload": "fulltime", "worker_id": 3},
                {"title":"Machine Learning Engineer", "compensation": 70000, "workload": "parttime", "worker_id": 3},
                {"title":"Python Data Scientist", "compensation": 80000, "workload": "parttime", "worker_id": 4},
                {"title":"Python Analyst", "compensation": 90000, "workload": "fulltime", "worker_id": 4},
                {"title":"Python Junior Developer", "compensation": 100000, "workload": "fulltime", "worker_id": 5},
            ]
            insert_workers = insert(WorkersOrm).values(workers)
            insert_resumes = insert(ResumesOrm).values(resumes)
            await session.execute(insert_workers)
            await session.execute(insert_resumes)
            await session.commit()
    """
        select
        	w.id,
        	w.username,
        	r.compensation,
        	r.workload,
        	avg(r.compensation) over (partition by workload)::int as avg_workload_compensation
        from resumes r
        join workers w on r.worker_id = w.id



        select *, compensation-avg_workload_compensation as compensation_diff
        from
        (select
        	w.id,
        	w.username,
        	r.compensation,
        	r.workload,
        	avg(r.compensation) over (partition by workload)::int as avg_workload_compensation
        from resumes r
        join workers w on r.worker_id = w.id) helper1



        With helper2 as(
        	select *, compensation-avg_workload_compensation as compensation_diff
        	from
        	(select
        		w.id,
        		w.username,
        		r.compensation,
        		r.workload,
        		avg(r.compensation) over (partition by workload)::int as avg_workload_compensation
        	from resumes r
        	join workers w on r.worker_id = w.id) helper1
        )
        select * from helper2
        order by compensation_diff desc
    """
    @staticmethod
    async def join_cte_subquery_window_func(like_language: str = "Python"):
        async with asyn_session_faktory() as session:
            """
                    With helper2 as(
                select *, compensation-avg_workload_compensation as compensation_diff
                from
                (select
                    w.id,
                    w.username,
                    r.compensation,
                    r.workload,
                    avg(r.compensation) over (partition by workload)::int as avg_workload_compensation
                from resumes r
                join workers w on r.worker_id = w.id) helper1
            )
            select * from helper2
            order by compensation_diff desc
            """
            r = aliased(ResumesOrm)
            w = aliased(WorkersOrm)
            subq = (
                select(
                    r,
                    w,
                    func.avg(r.compensation).over(partition_by=r.workload).cast(Integer).label("avg_workload_compensation"),
                )
                #.select_from(r)
                .join(r, r.worker_id == w.id).subquery("helper1")
            )
            cte = (
                select(
                    subq.c.worker_id,
                    subq.c.username,
                    subq.c.compensation,
                    subq.c.workload,
                    subq.c.avg_workload_compensation,
                    (subq.c.compensation - subq.c.avg_workload_compensation).label("compensation_diff"),
                ).subquery("helper2")
            )
            query = (
                select(cte)
                .order_by(cte.c.compensation_diff.desc())
            )
            #print(query.compile(compile_kwargs={"literal_binds": True}))
            res = await session.execute(query)
            result = res.all()
            print(f"{result=}")


















#"""
#for async sess 
#"""
#async def asyn_insert_data():
#    async with asyn_session_faktory() as asyn_session:
#        workers_bobr = WorkersOrm(username="Bobr")
#        workers_volk = WorkersOrm(username="Volk")
#        asyn_session.add_all([workers_bobr, workers_volk])
#        await asyn_session.commit()