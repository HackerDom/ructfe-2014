help:
	echo Targets: main-db test-db clean

main-db:
	psql -f game-databases-create.sql
	./run.sh ructfe2014 ructfe2014 tables-create.sql
	./run.sh ructfe2014 ructfe2014 ructfe2014-services.sql
	./run.sh ructfe2014 ructfe2014 game-teams-add.sql
	./change-owner.sh ructfe2014 ructfe2014

test-db:
	psql -f test-databases-create.sql
	./run.sh testuser ructfetest tables-create.sql
	./run.sh testuser ructfetest ructfe2014-services.sql
	./run.sh testuser ructfetest test-teams-add.sql
	./change-owner.sh ructfetest testuser

clean-main:
	./run.sh ructfe2014 ructfe2014 tables-clear.sql
	./run.sh ructfe2014 ructfe2014 ructfe2014-services.sql
	./run.sh ructfe2014 ructfe2014 game-teams-add.sql

clean-test:
	./run.sh testuser ructfetest tables-clear.sql
	./run.sh testuser ructfetest ructfe2014-services.sql
	./run.sh testuser ructfetest test-teams-add.sql
