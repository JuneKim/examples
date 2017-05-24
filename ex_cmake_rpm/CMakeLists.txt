cmake_minimum_required(VERSION 2.6)
project(ex_cmake_rpm)

set(SRCS
		src/example.c
)

#Bring the headers, such as Student.h into the project
include_directories(include)

# Add executable called "helloDemo" that is built from the source files
# "demo.cxx" and "demo_b.cxx". The extensions are automatically found.
add_executable (${PROJECT_NAME} ${SRCS})

# Link the executable to the Hello library. Since the Hello library has
# public include directories we will use those link directories when building
# helloDemo
#target_link_libraries (helloDemo LINK_PUBLIC Hello)



# Recurse into the "Hello" and "Demo" subdirectories. This does not actually
# cause another cmake executable to run. The same process will walk through
# the project's entire directory structure.
#add_subdirectory (Hello)
#add_subdirectory (Demo)
