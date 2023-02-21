from editor.common.pipeline import Pipeline

buildPipeline = Pipeline('prebuild', 'build', 'postbuild')

buildPipeline.registerTask(lambda dict: print(dict), 'build', 100)


buildPipeline.run()



# define registers