const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      '/api': {
        target: process.env.VUE_APP_API_URL || 'http://localhost:5000',
        changeOrigin: true,
        secure: false
      }
    }
  },
  chainWebpack: config => {
    config.plugin('define').tap(args => {
      args[0]['__VUE_PROD_HYDRATION_MISMATCH_DETAILS__'] = JSON.stringify(false)
      return args
    })

    const copyPlugin = config.plugin('copy')
    copyPlugin.tap(args => {
      const [options] = args
      if (options && Array.isArray(options.patterns)) {
        options.patterns = options.patterns.map(pattern => {
          if (pattern.globOptions) {
            pattern.globOptions = {
              ...pattern.globOptions,
              ignore: Array.isArray(pattern.globOptions.ignore)
                ? [...new Set([...pattern.globOptions.ignore, '**/index.html'])]
                : ['**/index.html']
            }
          } else {
            pattern.globOptions = {
              ignore: ['**/index.html']
            }
          }
          return pattern
        })
      }
      return args
    })
  }
})
