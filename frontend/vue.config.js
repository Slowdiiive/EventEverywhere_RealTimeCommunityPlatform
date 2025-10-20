module.exports = {
  publicPath: process.env.VUE_APP_PUBLIC_PATH,
  outputDir: "dist",
  assetsDir: "static",
  lintOnSave: true,
  productionSourceMap: false,
  devServer: {
    port: process.env.VUE_APP_PORT,
    open: false,
    proxy: {
      [process.env.VUE_APP_BASE_API]: {
        target: process.env.VUE_APP_PROXY_TARGET,
        changeOrigin: true,
        pathRewrite: {
          ['^' + process.env.VUE_APP_BASE_API]: ''
        },
      },
    },
  },
};
