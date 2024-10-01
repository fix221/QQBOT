import React from 'react'
import { Switch, Input, Button } from './ui/componets'

export default function ConfigInterface() {
  return (
    <div className="min-h-screen bg-gray-200 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-lg w-full max-w-3xl p-6">
        <h1 className="text-2xl font-bold mb-6 text-center">欢迎使用配置中心</h1>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <Switch id="port" defaultChecked />
              <label htmlFor="port" className="ml-2">配置 Nonebot 监听的端口</label>
            </div>
            <span className="text-green-500">8080</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-gray-600">PORT</span>
            <Input className="w-24" defaultValue="8080" />
          </div>
          <div className="flex items-center justify-between">
            <span className="flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
              </svg>
              配置 Nonebot 监听的 IP 地址
            </span>
            <span className="text-green-500">127.0.0.1</span>
          </div>
          <div className="flex items-center justify-between">
            <span>超级用户</span>
            <Input className="w-32" defaultValue="1925019494" />
          </div>
          <div className="flex items-center justify-between">
            <span>是否将所有的管理员视为超级用户</span>
            <Switch />
          </div>
          <div className="flex items-center justify-between">
            <span>指令分隔符</span>
            <Input className="w-24" />
          </div>
          <div className="flex items-center justify-between">
            <span>指令起始字符</span>
            <Input className="w-24" />
          </div>
          <div className="flex items-center justify-between">
            <span>日志输出等级</span>
            <span className="text-green-500">INFO</span>
          </div>
          <div className="flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
            </svg>
            <span>密钥</span>
          </div>
          <div className="flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
            </svg>
            <span>机器人平台的 AccessToken</span>
          </div>
        </div>
        <div className="mt-6 flex justify-end space-x-4">
          <Button variant="outline">恢复默认</Button>
          <Button variant="outline">获取原始配置</Button>
          <Button>保存一下</Button>
        </div>
      </div>
    </div>
  )
}