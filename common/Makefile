# based on Remi Collet's Makefile
# https://github.com/remicollet/remirepo

RPMDEFINES := --define "_sourcedir $(SRCDIR)" \
              --define "_specdir $(SRCDIR)" \
              --define "_srcrpmdir $(SRCDIR)" \
              --define "_rpmdir $(SRCDIR)"

SRCDEFINES := --define "dist .sl" \
              --define "_source_filedigest_algorithm 1" \
              --define "_binary_filedigest_algorithm 1"

arch:
	cp -rfv noarch x86_64 i386 i686 *.src.rpm ../RPMS/ && echo done || echo Nothing to do

clean:
	@echo Clean $(NAME) in $(SRCDIR)
	@rm -rfv *~ noarch x86_64 i386 i686 *.src.rpm

srpm:
	rpmbuild $(RPMDEFINES) $(SRCDEFINES) -bs $(NAME).spec

devsrpm:
	rpmbuild $(RPMDEFINES) $(SRCDEFINES) -bs $(NAME)-dev.spec

build:
	rpmbuild $(RPMDEFINES) -bb $(NAME).spec

buildmini:
	rpmbuild $(RPMDEFINES) --define "runselftest 0" -bb $(NAME).spec

bp:
	rpmbuild $(RPMDEFINES) -bp $(NAME).spec

bc:
	rpmbuild $(RPMDEFINES) -bc --short-circuit $(NAME).spec

bi:
	rpmbuild $(RPMDEFINES) -bi --short-circuit $(NAME).spec

devbp:
	rpmbuild $(RPMDEFINES)  --define "runselftest 0" -bp $(NAME)-dev.spec

devbi:
	rpmbuild $(RPMDEFINES)  --define "runselftest 0" -bi --short-circuit $(NAME)-dev.spec

devbl:
	rpmbuild $(RPMDEFINES) -bl --short-circuit $(NAME)-dev.spec

bl:
	rpmbuild $(RPMDEFINES) -bl --short-circuit $(NAME).spec

devbuild:
	rpmbuild $(RPMDEFINES) -bb $(NAME)-dev.spec

devbuildmini:
	rpmbuild $(RPMDEFINES) --define "runselftest 0" -bb $(NAME)-dev.spec

sign:
	rpmsign --addsign *.src.rpm

signall:
	find . -type f -name '*.rpm' -exec rpmsign --addsign {} \;
