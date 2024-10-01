import React from 'react'

export const Switch: React.FC<React.InputHTMLAttributes<HTMLInputElement>> = (props) => {
  return (
    <label className="relative inline-flex items-center cursor-pointer">
      <input type="checkbox" className="sr-only peer" {...props} />
      <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
    </label>
  )
}

export const Input: React.FC<React.InputHTMLAttributes<HTMLInputElement>> = (props) => {
  return (
    <input
      className="border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
      {...props}
    />
  )
}

export const Button: React.FC<React.ButtonHTMLAttributes<HTMLButtonElement> & {variant?: 'default' | 'outline'}> = ({ children, variant = 'default', ...props }) => {
  const baseClasses = "px-4 py-2 rounded-md font-medium focus:outline-none focus:ring-2 focus:ring-blue-500"
  const variantClasses = variant === 'outline' 
    ? "border border-gray-300 text-gray-700 hover:bg-gray-50" 
    : "bg-blue-600 text-white hover:bg-blue-700"
  
  return (
    <button className={`${baseClasses} ${variantClasses}`} {...props}>
      {children}
    </button>
  )
}