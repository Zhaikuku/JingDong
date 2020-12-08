-- 192.168.0.13 
use [crawl]
-- alter table DerKang add id

------------------------
-- 处理德尔康信息，将 [ShangPinName] 列分隔 写入 DaiFenxi 表 对比数据时 使用 like [PinMing]
declare @Pinming varchar(50),@name varchar(200),@changjia varchar(100),@jiage varchar(100),@xiaoliang varchar(100),@gongsimingcheng int
declare cursor1 cursor  for 
select  ShangPinName,ShangPinName,ShengChanChangJia,JiaGe,XiaoLiang from DerKang
open cursor1	
fetch next from cursor1 into @Pinming,@name,@changjia,@jiage,@xiaoliang,@gongsimingcheng 
while @@FETCH_STATUS = 0  
begin  
declare  @Fenge nvarchar(100),
	@GG varchar(30),
	@PM varchar(30)
set @Fenge  = @Pinming
	select @GG= substring(@Fenge,charindex(' ',@Fenge,1)+1,len(@Fenge)-charindex(' ',@Fenge,1)+1)

	select @PM = SUBSTRING(@Fenge,1,3)

	insert into  DaiFenxi  select @GG,@PM ,@name,@changjia,@jiage,@xiaoliang,@gongsimingcheng
	

fetch next from cursor1 into  @Pinming,@name,@changjia,@jiage,@xiaoliang,@gongsimingcheng 
end
close cursor1 
deallocate cursor1 
-- select * from  DaiFenxi
-- TRUNCATE TABLE DaiFenxi

-----------------------------------------
-- 写入192.168.0.84
/*
declare @Pinming varchar(50),@name varchar(200),@changjia varchar(100),@jiage varchar(100),@xiaoliang varchar(100),@gongsimingcheng int
declare cursor1 cursor  for 
select  ShangPinName,ShangPinName,ShengChanChangJia,JiaGe,XiaoLiang,GongSiMingCheng from SourceData where GongSiMingCheng = 3
open cursor1	
fetch next from cursor1 into @Pinming,@name,@changjia,@jiage,@xiaoliang,@gongsimingcheng
while @@FETCH_STATUS = 0  
begin  
declare  @Fenge nvarchar(100),
	@GG varchar(30),
	@PM varchar(30)
set @Fenge  = @Pinming
	select @GG= substring(@Fenge,charindex(' ',@Fenge,1)+1,len(@Fenge)-charindex(' ',@Fenge,1)+1)

	select @PM = SUBSTRING(@Fenge,1,3)

	insert into  [192.168.0.84].BI_2.dbo.DaiFenxi  select @GG,@PM ,@name,@changjia,@jiage,@xiaoliang,@gongsimingcheng
	

fetch next from cursor1 into  @Pinming,@name,@changjia,@jiage,@xiaoliang,@gongsimingcheng
end
close cursor1 
deallocate cursor1  
*/
-----------------------------------------
-----------------------------------------

--处理恩济信息 写入 enji

declare @spid varchar(20)
declare cursor1 cursor  for 
select distinct spid  from [192.168.0.84].ksoa.dbo.ds_spkfk
open cursor1	
fetch next from cursor1 into @spid
while @@FETCH_STATUS = 0  
begin   
insert into  enji
select top 1 c.zdshj,b.kcshl,a.spbh,a.shengccj,a.shpgg,a.spmch from [192.168.0.84].ksoa.dbo.spkfk a
join [192.168.0.84].ksoa.dbo.spkfjc b on a.spid= b.spid
join [192.168.0.84].ksoa.dbo.sphwph as c on b.spid = c.spid
join [192.168.0.84].ksoa.dbo.ds_spkfk as d on a.spid = c.spid
where a.spid =@spid
and b.kcshl > 1   order by c.zdshj desc

fetch next from cursor1 into @spid
end
close cursor1 
deallocate cursor1 


-- select * from enji
-- TRUNCATE TABLE enji
------------------------------------------
--对比数据
declare @Pinming1 varchar(20)
declare cursor1 cursor  for 
select  distinct PinMing from DaiFenxi
open cursor1	
fetch next from cursor1 into @Pinming1
while @@FETCH_STATUS = 0  
begin   
insert into DuiBi
select  b.zdshj as [恩济A价格],a.JiaGe as[德尔康价格],b.spbh as[商品编号],b.spmch as [恩济商品名],a.ShangPinName as[德尔康品名],b.shengccj as [恩济生产厂家],a.ShengChanChangJia as [德尔康生产厂家],b.shpgg as [恩济规格],a.Guige as [德尔康规格],a.PinMing as [匹配规则]
from DaiFenxi as a join enji b 
on a.Guige = b.shpgg and a.ShengChanChangJia = b.shengccj
where b.spmch like '%'+@Pinming1+'%'
and a.PinMing like   '%'+@Pinming1+'%'
and a.XiaoLiang != '缺'

fetch next from cursor1 into @Pinming1
end
close cursor1 
deallocate cursor1 

-- select * from enji
-- TRUNCATE TABLE DuiBi
-----------------------------------------
select zdshj as [恩济A价格],JiaGe as[德尔康价格],spbh as[商品编号],spmch as [恩济商品名],PinMing as[德尔康品名],piPeiguize as [匹配规则],shengccj as [恩济生产厂家],ShengChanChangJia as [德尔康生产厂家],shpgg as [恩济规格],Guige as [德尔康规格] 
from DuiBi(nolock)  order by zdshj 




-----------------------
-- 根据 spbh 查 恩济信息 top 1 查最高价
select  c.zdshj,b.kcshl,a.spbh,a.shengccj,a.shpgg,a.spmch from [192.168.0.84].ksoa.dbo.spkfk a
join [192.168.0.84].ksoa.dbo.spkfjc b on a.spid= b.spid
join [192.168.0.84].ksoa.dbo.sphwph as c on b.spid = c.spid
join [192.168.0.84].ksoa.dbo.ds_spkfk as d on a.spid = c.spid
where a.spbh ='3161856'
and b.kcshl > 1   order by c.zdshj desc
-----------------------