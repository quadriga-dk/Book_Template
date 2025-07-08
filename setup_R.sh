# /usr/bin/env bash
#
# Run after installing or upgrading R
#
# This command makes sure, that the R kernel is installed and registered.

Rscript -e 'options(repos = c(CRAN = "https://cloud.r-project.org")); install.packages("IRkernel", dependencies=TRUE); IRkernel::installspec(name="ir", displayname="R")'
