-- 192.168.0.13 
use [crawl]
-- alter table DerKang add id

------------------------
-- ����¶�����Ϣ���� [ShangPinName] �зָ� д�� DaiFenxi �� �Ա�����ʱ ʹ�� like [PinMing]
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
-- д��192.168.0.84
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

--���������Ϣ д�� enji

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
--�Ա�����
declare @Pinming1 varchar(20)
declare cursor1 cursor  for 
select  distinct PinMing from DaiFenxi
open cursor1	
fetch next from cursor1 into @Pinming1
while @@FETCH_STATUS = 0  
begin   
insert into DuiBi
select  b.zdshj as [����A�۸�],a.JiaGe as[�¶����۸�],b.spbh as[��Ʒ���],b.spmch as [������Ʒ��],a.ShangPinName as[�¶���Ʒ��],b.shengccj as [������������],a.ShengChanChangJia as [�¶�����������],b.shpgg as [���ù��],a.Guige as [�¶������],a.PinMing as [ƥ�����]
from DaiFenxi as a join enji b 
on a.Guige = b.shpgg and a.ShengChanChangJia = b.shengccj
where b.spmch like '%'+@Pinming1+'%'
and a.PinMing like   '%'+@Pinming1+'%'
and a.XiaoLiang != 'ȱ'

fetch next from cursor1 into @Pinming1
end
close cursor1 
deallocate cursor1 

-- select * from enji
-- TRUNCATE TABLE DuiBi
-----------------------------------------
select zdshj as [����A�۸�],JiaGe as[�¶����۸�],spbh as[��Ʒ���],spmch as [������Ʒ��],PinMing as[�¶���Ʒ��],piPeiguize as [ƥ�����],shengccj as [������������],ShengChanChangJia as [�¶�����������],shpgg as [���ù��],Guige as [�¶������] 
from DuiBi(nolock)  order by zdshj 




-----------------------
-- ���� spbh �� ������Ϣ top 1 ����߼�
select  c.zdshj,b.kcshl,a.spbh,a.shengccj,a.shpgg,a.spmch from [192.168.0.84].ksoa.dbo.spkfk a
join [192.168.0.84].ksoa.dbo.spkfjc b on a.spid= b.spid
join [192.168.0.84].ksoa.dbo.sphwph as c on b.spid = c.spid
join [192.168.0.84].ksoa.dbo.ds_spkfk as d on a.spid = c.spid
where a.spbh ='3161856'
and b.kcshl > 1   order by c.zdshj desc
-----------------------