import { useEffect, useRef } from 'react'
import * as THREE from 'three'

export default function Preview3D() {
  const mountRef = useRef(null)

  useEffect(() => {
    const width = mountRef.current.clientWidth
    const height = 260
    const scene = new THREE.Scene()
    scene.background = new THREE.Color('#0a0a0a')

    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000)
    camera.position.set(0, 1, 6)

    const renderer = new THREE.WebGLRenderer({ antialias: true })
    renderer.setSize(width, height)
    mountRef.current.appendChild(renderer.domElement)

    const light = new THREE.DirectionalLight(0xffffff, 1)
    light.position.set(3, 3, 4)
    scene.add(light)

    const mannequin = new THREE.Mesh(
      new THREE.CapsuleGeometry(1, 2.3, 8, 16),
      new THREE.MeshStandardMaterial({ color: '#b8b8b8', metalness: 0.3, roughness: 0.5 }),
    )
    scene.add(mannequin)

    const garment = new THREE.Mesh(
      new THREE.CylinderGeometry(1.3, 1.1, 2, 32),
      new THREE.MeshStandardMaterial({ color: '#111827', wireframe: true }),
    )
    garment.position.y = 0.2
    scene.add(garment)

    const animate = () => {
      garment.rotation.y += 0.008
      mannequin.rotation.y += 0.005
      renderer.render(scene, camera)
      requestAnimationFrame(animate)
    }
    animate()

    return () => {
      renderer.dispose()
      if (mountRef.current?.contains(renderer.domElement)) mountRef.current.removeChild(renderer.domElement)
    }
  }, [])

  return <div ref={mountRef} className="w-full rounded-xl border border-zinc-700" />
}
